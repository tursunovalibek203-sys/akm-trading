from pydantic import BaseModel, field_validator
from typing import Literal
import uuid
from datetime import datetime


class ZoneCreateRequest(BaseModel):
    symbol: str
    zone_type: Literal["support", "resistance", "demand", "supply"]
    price_from: float
    price_to: float
    label: str | None = None

    @field_validator("symbol")
    @classmethod
    def validate_symbol(cls, v: str) -> str:
        return v.upper().strip()

    @field_validator("price_to")
    @classmethod
    def validate_price_range(cls, v: float, info) -> float:
        price_from = info.data.get("price_from")
        if price_from is not None and v <= price_from:
            raise ValueError("price_to price_from dan katta bo'lishi kerak")
        return v


class ZoneUpdateRequest(BaseModel):
    zone_type: Literal["support", "resistance", "demand", "supply"] | None = None
    price_from: float | None = None
    price_to: float | None = None
    label: str | None = None
    is_active: bool | None = None


class ZoneResponse(BaseModel):
    id: str
    user_id: str
    symbol: str
    zone_type: str
    price_from: float
    price_to: float
    label: str | None
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}

    @classmethod
    def from_orm_model(cls, obj) -> "ZoneResponse":
        return cls(
            id=str(obj.id),
            user_id=str(obj.user_id),
            symbol=obj.symbol,
            zone_type=obj.zone_type.value,
            price_from=float(obj.price_from),
            price_to=float(obj.price_to),
            label=obj.label,
            is_active=obj.is_active,
            created_at=obj.created_at,
        )
