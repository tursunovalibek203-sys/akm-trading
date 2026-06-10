import json
from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect, Depends
from app.core.redis import get_redis
from app.core.logger import logger

router = APIRouter(prefix="/market", tags=["market"])

SUPPORTED_SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]


@router.get("/symbols")
async def get_symbols():
    return {"symbols": SUPPORTED_SYMBOLS}


@router.get("/price/{symbol}")
async def get_price(symbol: str, redis=Depends(get_redis)):
    symbol = symbol.upper()
    if symbol not in SUPPORTED_SYMBOLS:
        raise HTTPException(status_code=404, detail=f"{symbol} qo'llab-quvvatlanmaydi")

    cached = await redis.get(f"price:{symbol}")
    if not cached:
        raise HTTPException(status_code=503, detail="Narx ma'lumoti hali yuklanmadi")

    return json.loads(cached)


@router.get("/klines/{symbol}")
async def get_klines(symbol: str, interval: str = "1m", limit: int = 100, redis=Depends(get_redis)):
    symbol = symbol.upper()
    if symbol not in SUPPORTED_SYMBOLS:
        raise HTTPException(status_code=404, detail=f"{symbol} qo'llab-quvvatlanmaydi")

    raw_list = await redis.lrange(f"klines:{symbol}:{interval}", 0, limit - 1)
    if not raw_list:
        raise HTTPException(status_code=503, detail="Kline ma'lumoti hali yuklanmadi")

    return {"symbol": symbol, "interval": interval, "candles": [json.loads(c) for c in raw_list]}


@router.websocket("/ws/{symbol}")
async def websocket_price(websocket: WebSocket, symbol: str, redis=Depends(get_redis)):
    symbol = symbol.upper()
    await websocket.accept()
    logger.info(f"WebSocket ulandi: {symbol}")
    try:
        import asyncio
        while True:
            cached = await redis.get(f"price:{symbol}")
            if cached:
                await websocket.send_text(cached)
            await asyncio.sleep(0.5)
    except WebSocketDisconnect:
        logger.info(f"WebSocket uzildi: {symbol}")
