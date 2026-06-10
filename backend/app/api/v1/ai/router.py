import json
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.api.v1.auth.dependencies import get_current_user
from app.core.redis import get_redis
from app.services.ai.signal_analyzer import analyze_signal
from app.core.logger import logger

router = APIRouter(prefix="/ai", tags=["ai"])


class SignalRequest(BaseModel):
    symbol: str
    timeframe: str = "1h"


class SignalResponse(BaseModel):
    symbol: str
    direction: str
    confidence: float
    score: int
    signal_quality: str
    reasoning: str
    details: dict


@router.post("/analyze", response_model=SignalResponse)
async def analyze(
    payload: SignalRequest,
    current_user=Depends(get_current_user),
    redis=Depends(get_redis),
):
    symbol = payload.symbol.upper()

    # Narx va kline ma'lumotlarini Redis dan olish
    price_raw = await redis.get(f"price:{symbol}")
    klines_raw = await redis.lrange(f"klines:{symbol}:{payload.timeframe}", 0, 99)

    if not price_raw:
        raise HTTPException(status_code=503, detail=f"{symbol} narxi hali yuklanmadi")
    if len(klines_raw) < 10:
        raise HTTPException(status_code=503, detail=f"{symbol} kline ma'lumoti yetarli emas")

    price_data = json.loads(price_raw)
    current_price = float(price_data.get("ask", 0))
    candles = [json.loads(c) for c in klines_raw]

    logger.info(f"AI tahlil boshlandi: {symbol} {payload.timeframe} (foydalanuvchi: {current_user.email})")

    result = await analyze_signal(
        symbol=symbol,
        candles=candles,
        current_price=current_price,
        timeframe=payload.timeframe,
    )

    return SignalResponse(
        symbol=symbol,
        direction=result.direction,
        confidence=result.confidence,
        score=result.score,
        signal_quality=result.signal_quality,
        reasoning=result.reasoning,
        details=result.details,
    )
