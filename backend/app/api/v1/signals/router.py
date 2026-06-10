import json
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid

from app.core.database import get_db
from app.core.redis import get_redis
from app.core.logger import logger
from app.models.signal import Signal, SignalDirection, SignalStatus
from app.models.trading_zone import TradingZone
from app.schemas.signal import SignalCreateRequest, SignalStatusUpdateRequest, SignalResponse
from app.api.v1.auth.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/signals", tags=["signals"])

_signal_connections: dict[str, list[WebSocket]] = {}


@router.post("", response_model=SignalResponse, status_code=status.HTTP_201_CREATED)
async def create_signal(
    payload: SignalCreateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    redis=Depends(get_redis),
) -> SignalResponse:
    zone_uuid: uuid.UUID | None = None
    if payload.zone_id:
        try:
            zone_uuid = uuid.UUID(payload.zone_id)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Noto'g'ri zone_id")
        zone_check = await db.execute(
            select(TradingZone).where(
                TradingZone.id == zone_uuid,
                TradingZone.user_id == current_user.id,
            )
        )
        if not zone_check.scalar_one_or_none():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Zona topilmadi")

    signal = Signal(
        user_id=current_user.id,
        zone_id=zone_uuid,
        symbol=payload.symbol,
        direction=SignalDirection(payload.direction),
        entry_price=payload.entry_price,
        stop_loss=payload.stop_loss,
        take_profit_1=payload.take_profit_1,
        take_profit_2=payload.take_profit_2,
        reasoning=payload.reasoning,
    )
    db.add(signal)
    await db.commit()
    await db.refresh(signal)

    response = SignalResponse.from_orm_model(signal)
    await _broadcast_signal(str(current_user.id), response, redis)
    logger.info(f"Signal yaratildi: {signal.id} | {signal.symbol} | {payload.direction}")
    return response


@router.get("", response_model=list[SignalResponse])
async def get_signals(
    symbol: str | None = None,
    direction: str | None = None,
    status_filter: str | None = Query(default=None, alias="status"),
    limit: int = Query(default=50, le=200),
    offset: int = Query(default=0, ge=0),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[SignalResponse]:
    query = select(Signal).where(Signal.user_id == current_user.id)
    if symbol:
        query = query.where(Signal.symbol == symbol.upper())
    if direction and direction in ("long", "short"):
        query = query.where(Signal.direction == SignalDirection(direction))
    if status_filter:
        try:
            query = query.where(Signal.status == SignalStatus(status_filter))
        except ValueError:
            pass
    query = query.order_by(Signal.created_at.desc()).limit(limit).offset(offset)

    result = await db.execute(query)
    signals = result.scalars().all()
    return [SignalResponse.from_orm_model(s) for s in signals]


@router.patch("/{signal_id}/status", response_model=SignalResponse)
async def update_signal_status(
    signal_id: str,
    payload: SignalStatusUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> SignalResponse:
    try:
        signal_uuid = uuid.UUID(signal_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Noto'g'ri signal_id")

    result = await db.execute(
        select(Signal).where(Signal.id == signal_uuid, Signal.user_id == current_user.id)
    )
    signal = result.scalar_one_or_none()
    if not signal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Signal topilmadi")

    signal.status = SignalStatus(payload.status)
    await db.commit()
    await db.refresh(signal)
    return SignalResponse.from_orm_model(signal)


@router.delete("/{signal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_signal(
    signal_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    try:
        signal_uuid = uuid.UUID(signal_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Noto'g'ri signal_id")

    result = await db.execute(
        select(Signal).where(Signal.id == signal_uuid, Signal.user_id == current_user.id)
    )
    signal = result.scalar_one_or_none()
    if not signal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Signal topilmadi")

    await db.delete(signal)
    await db.commit()


@router.websocket("/ws")
async def signal_websocket(websocket: WebSocket, token: str, redis=Depends(get_redis)):
    from app.core.security import decode_token
    try:
        payload = decode_token(token)
        if payload.get("type") != "access":
            await websocket.close(code=4001)
            return
        user_id = payload.get("sub")
        if not user_id:
            await websocket.close(code=4001)
            return
    except Exception:
        await websocket.close(code=4001)
        return

    await websocket.accept()
    if user_id not in _signal_connections:
        _signal_connections[user_id] = []
    _signal_connections[user_id].append(websocket)
    logger.info(f"Signal WS ulandi: user={user_id}")

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        _signal_connections.get(user_id, []).remove(websocket) if websocket in _signal_connections.get(user_id, []) else None
        logger.info(f"Signal WS uzildi: user={user_id}")


async def _broadcast_signal(user_id: str, signal: SignalResponse, redis) -> None:
    connections = _signal_connections.get(user_id, [])
    if not connections:
        return
    payload = signal.model_dump_json()
    dead: list[WebSocket] = []
    for ws in connections:
        try:
            await ws.send_text(payload)
        except Exception:
            dead.append(ws)
    for ws in dead:
        connections.remove(ws)
