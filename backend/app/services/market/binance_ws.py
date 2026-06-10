import asyncio
import json
import websockets
from app.core.logger import logger
from app.core.config import settings
from app.core.redis import get_redis

SUPPORTED_SYMBOLS = ["btcusdt", "ethusdt", "bnbusdt", "solusdt", "xrpusdt"]
KLINE_INTERVALS = ["1m", "5m", "15m", "1h", "4h"]


async def _stream_price(symbol: str, redis) -> None:
    url = f"{settings.BINANCE_WS_URL}/ws/{symbol}@bookTicker"
    retry = 0
    max_retries = 5

    while retry < max_retries:
        try:
            async with websockets.connect(url, ping_interval=20) as ws:
                logger.info(f"Binance WS ulandi: {symbol}@bookTicker")
                retry = 0
                async for raw in ws:
                    data = json.loads(raw)
                    price = {
                        "symbol": data["s"],
                        "bid": data["b"],
                        "ask": data["a"],
                    }
                    sym_upper = symbol.upper()
                    await redis.setex(f"price:{sym_upper}", 10, json.dumps(price))
                    await _check_zone_triggers(sym_upper, float(data["a"]), redis)
        except Exception as e:
            retry += 1
            wait = 2 ** retry
            logger.warning(f"WS uzildi ({symbol}), {wait}s... [{retry}/{max_retries}]: {e}")
            await asyncio.sleep(wait)

    logger.error(f"WS {symbol} uchun {max_retries} urinishdan so'ng to'xtatildi")


async def _stream_klines(symbol: str, interval: str, redis) -> None:
    url = f"{settings.BINANCE_WS_URL}/ws/{symbol}@kline_{interval}"
    retry = 0

    while retry < 5:
        try:
            async with websockets.connect(url, ping_interval=20) as ws:
                logger.info(f"Kline stream ulandi: {symbol} {interval}")
                retry = 0
                async for raw in ws:
                    data = json.loads(raw)
                    k = data["k"]
                    candle = {
                        "t": k["t"], "o": k["o"], "h": k["h"],
                        "l": k["l"], "c": k["c"], "v": k["v"],
                        "closed": k["x"],
                    }
                    sym_upper = symbol.upper()
                    key = f"klines:{sym_upper}:{interval}"
                    # Har doim oxirgi sham yangilanadi (open candle), yopilganda ro'yxatga qo'shiladi
                    await redis.lset_or_push(key, candle, k["x"])
                    if k["x"]:
                        await redis.lpush(key, json.dumps(candle))
                        await redis.ltrim(key, 0, 499)
        except AttributeError:
            # lset_or_push yo'q — oddiy usul
            async with websockets.connect(url, ping_interval=20) as ws:
                retry = 0
                async for raw in ws:
                    data = json.loads(raw)
                    k = data["k"]
                    if k["x"]:
                        candle = {
                            "t": k["t"], "o": k["o"], "h": k["h"],
                            "l": k["l"], "c": k["c"], "v": k["v"],
                        }
                        sym_upper = symbol.upper()
                        key = f"klines:{sym_upper}:{interval}"
                        await redis.lpush(key, json.dumps(candle))
                        await redis.ltrim(key, 0, 499)
        except Exception as e:
            retry += 1
            await asyncio.sleep(2 ** retry)
            logger.warning(f"Kline WS xato ({symbol} {interval}): {e}")


async def _check_zone_triggers(symbol: str, current_price: float, redis) -> None:
    """Narx zona ichiga kirganini tekshiradi va signal yaratadi."""
    try:
        zones_raw = await redis.get(f"zones:{symbol}")
        if not zones_raw:
            return

        zones: list[dict] = json.loads(zones_raw)
        for zone in zones:
            if not zone.get("is_active"):
                continue

            price_from = float(zone["price_from"])
            price_to = float(zone["price_to"])

            if price_from <= current_price <= price_to:
                zone_id = zone["id"]
                user_id = zone["user_id"]
                debounce_key = f"zone_trigger:{zone_id}"

                # 5 daqiqada bir marta signal yaratish (debounce)
                already_triggered = await redis.get(debounce_key)
                if already_triggered:
                    continue

                await redis.setex(debounce_key, 300, "1")

                direction = "long" if zone["zone_type"] in ("support", "demand") else "short"
                signal = {
                    "user_id": user_id,
                    "zone_id": zone_id,
                    "symbol": symbol,
                    "direction": direction,
                    "entry_price": current_price,
                    "source": "zone_trigger",
                }

                # Signal queue ga qo'shish (DB operatsiyasi background task orqali)
                await redis.lpush("signal_queue", json.dumps(signal))
                logger.info(f"Zona trigger: {symbol} {zone['zone_type']} @ {current_price:.4f}")

    except Exception as e:
        logger.debug(f"Zone trigger xato ({symbol}): {e}")


async def _process_signal_queue(redis) -> None:
    """Redis queue'dan signallarni o'qib DB ga yozadi."""
    from app.core.database import AsyncSessionLocal
    from app.models.signal import Signal, SignalDirection

    while True:
        try:
            raw = await redis.brpop("signal_queue", timeout=5)
            if not raw:
                await asyncio.sleep(1)
                continue

            _, data_str = raw
            data = json.loads(data_str)

            async with AsyncSessionLocal() as db:
                import uuid
                signal = Signal(
                    user_id=uuid.UUID(data["user_id"]),
                    zone_id=uuid.UUID(data["zone_id"]) if data.get("zone_id") else None,
                    symbol=data["symbol"],
                    direction=SignalDirection(data["direction"]),
                    entry_price=data["entry_price"],
                    reasoning=f"Zona trigger: {data['symbol']} narxi zonaga kirdi",
                )
                db.add(signal)
                await db.commit()
                logger.info(f"Zona trigger signal DB ga yozildi: {data['symbol']}")

        except Exception as e:
            logger.error(f"Signal queue xato: {e}")
            await asyncio.sleep(2)


async def refresh_zones_cache(redis) -> None:
    """Har 30 soniyada barcha aktiv zonalarni Redis ga kesh qiladi."""
    from app.core.database import AsyncSessionLocal
    from app.models.trading_zone import TradingZone
    from sqlalchemy import select

    while True:
        try:
            async with AsyncSessionLocal() as db:
                result = await db.execute(
                    select(TradingZone).where(TradingZone.is_active.is_(True))
                )
                zones = result.scalars().all()

                zones_by_symbol: dict[str, list] = {}
                for z in zones:
                    sym = z.symbol.upper()
                    if sym not in zones_by_symbol:
                        zones_by_symbol[sym] = []
                    zones_by_symbol[sym].append({
                        "id": str(z.id),
                        "user_id": str(z.user_id),
                        "zone_type": z.zone_type.value,
                        "price_from": float(z.price_from),
                        "price_to": float(z.price_to),
                        "is_active": z.is_active,
                    })

                for sym, zone_list in zones_by_symbol.items():
                    await redis.setex(f"zones:{sym}", 60, json.dumps(zone_list))

        except Exception as e:
            logger.warning(f"Zones cache refresh xato: {e}")

        await asyncio.sleep(30)


async def start_market_streams() -> None:
    redis = await get_redis()
    tasks: list[asyncio.Task] = []

    for symbol in SUPPORTED_SYMBOLS:
        tasks.append(asyncio.create_task(_stream_price(symbol, redis)))
        for interval in KLINE_INTERVALS:
            tasks.append(asyncio.create_task(_stream_klines(symbol, interval, redis)))

    tasks.append(asyncio.create_task(_process_signal_queue(redis)))
    tasks.append(asyncio.create_task(refresh_zones_cache(redis)))

    logger.info(f"Market stream tasklari ishga tushdi: {len(tasks)} ta ({len(SUPPORTED_SYMBOLS)} symbol × {len(KLINE_INTERVALS)} interval)")
