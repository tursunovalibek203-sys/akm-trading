from pydantic import BaseModel, field_validator
from typing import Literal
from datetime import datetime


class SignalCreateRequest(BaseModel):
    symbol: str
    direction: Literal["long", "short"]
    entry_price: float
    stop_loss: float | None = None
    take_profit_1: float | None = None
    take_profit_2: float | None = None
    zone_id: str | None = None
    reasoning: str | None = None

    @field_validator("symbol")
    @classmethod
    def validate_symbol(cls, v: str) -> str:
        return v.upper().strip()

    @field_validator("entry_price")
    @classmethod
    def validate_entry_price(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("entry_price noldan katta bo'lishi kerak")
        return v


class SignalStatusUpdateRequest(BaseModel):
    status: Literal["active", "tp1_hit", "tp2_hit", "sl_hit", "cancelled", "expired"]


class SignalResponse(BaseModel):
    id: str
    user_id: str
    zone_id: str | None
    symbol: str
    direction: str
    score: int | None
    entry_price: float
    stop_loss: float | None
    take_profit_1: float | None
    take_profit_2: float | None
    status: str
    reasoning: str | None
    created_at: datetime

    model_config = {"from_attributes": True}

    @classmethod
    def from_orm_model(cls, obj) -> "SignalResponse":
        return cls(
            id=str(obj.id),
            user_id=str(obj.user_id),
            zone_id=str(obj.zone_id) if obj.zone_id else None,
            symbol=obj.symbol,
            direction=obj.direction.value,
            score=obj.score,
            entry_price=float(obj.entry_price),
            stop_loss=float(obj.stop_loss) if obj.stop_loss else None,
            take_profit_1=float(obj.take_profit_1) if obj.take_profit_1 else None,
            take_profit_2=float(obj.take_profit_2) if obj.take_profit_2 else None,
            status=obj.status.value,
            reasoning=obj.reasoning,
            created_at=obj.created_at,
        )
