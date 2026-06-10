from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class ServiceResult(BaseModel, Generic[T]):
    success: bool
    data: T | None = None
    error: str | None = None
    error_code: str | None = None

    @classmethod
    def ok(cls, data: T) -> "ServiceResult[T]":
        return cls(success=True, data=data)

    @classmethod
    def fail(cls, error: str, error_code: str = "ERROR") -> "ServiceResult[T]":
        return cls(success=False, error=error, error_code=error_code)
