from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid

from app.core.database import get_db
from app.core.logger import logger
from app.models.trading_zone import TradingZone, ZoneType
from app.schemas.zone import ZoneCreateRequest, ZoneUpdateRequest, ZoneResponse
from app.api.v1.auth.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/zones", tags=["zones"])


@router.post("", response_model=ZoneResponse, status_code=status.HTTP_201_CREATED)
async def create_zone(
    payload: ZoneCreateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ZoneResponse:
    zone = TradingZone(
        user_id=current_user.id,
        symbol=payload.symbol,
        zone_type=ZoneType(payload.zone_type),
        price_from=payload.price_from,
        price_to=payload.price_to,
        label=payload.label,
    )
    db.add(zone)
    await db.commit()
    await db.refresh(zone)
    logger.info(f"Zona yaratildi: {zone.id} | {zone.symbol} | {payload.zone_type}")
    return ZoneResponse.from_orm_model(zone)


@router.get("", response_model=list[ZoneResponse])
async def get_zones(
    symbol: str | None = None,
    active_only: bool = True,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[ZoneResponse]:
    query = select(TradingZone).where(TradingZone.user_id == current_user.id)
    if symbol:
        query = query.where(TradingZone.symbol == symbol.upper())
    if active_only:
        query = query.where(TradingZone.is_active.is_(True))
    query = query.order_by(TradingZone.created_at.desc()).limit(100)

    result = await db.execute(query)
    zones = result.scalars().all()
    return [ZoneResponse.from_orm_model(z) for z in zones]


@router.put("/{zone_id}", response_model=ZoneResponse)
async def update_zone(
    zone_id: str,
    payload: ZoneUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ZoneResponse:
    try:
        zone_uuid = uuid.UUID(zone_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Noto'g'ri zone_id format")

    result = await db.execute(
        select(TradingZone).where(
            TradingZone.id == zone_uuid,
            TradingZone.user_id == current_user.id,
        )
    )
    zone = result.scalar_one_or_none()
    if not zone:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Zona topilmadi")

    if payload.zone_type is not None:
        zone.zone_type = ZoneType(payload.zone_type)
    if payload.price_from is not None:
        zone.price_from = payload.price_from
    if payload.price_to is not None:
        zone.price_to = payload.price_to
    if payload.label is not None:
        zone.label = payload.label
    if payload.is_active is not None:
        zone.is_active = payload.is_active

    await db.commit()
    await db.refresh(zone)
    return ZoneResponse.from_orm_model(zone)


@router.delete("/{zone_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_zone(
    zone_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    try:
        zone_uuid = uuid.UUID(zone_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Noto'g'ri zone_id format")

    result = await db.execute(
        select(TradingZone).where(
            TradingZone.id == zone_uuid,
            TradingZone.user_id == current_user.id,
        )
    )
    zone = result.scalar_one_or_none()
    if not zone:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Zona topilmadi")

    await db.delete(zone)
    await db.commit()
    logger.info(f"Zona o'chirildi: {zone_id}")
