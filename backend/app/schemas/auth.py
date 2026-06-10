from pydantic import BaseModel, EmailStr, field_validator
import re


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 12:
            raise ValueError("Parol kamida 12 ta belgidan iborat bo'lishi kerak")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Parolda kamida 1 ta katta harf bo'lishi kerak")
        if not re.search(r"[a-z]", v):
            raise ValueError("Parolda kamida 1 ta kichik harf bo'lishi kerak")
        if not re.search(r"\d", v):
            raise ValueError("Parolda kamida 1 ta raqam bo'lishi kerak")
        return v


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    totp_code: str | None = None
    remember_me: bool = False


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


class TwoFactorSetupResponse(BaseModel):
    secret: str
    qr_code_url: str
    backup_codes: list[str]


class TwoFactorVerifyRequest(BaseModel):
    code: str


class UserResponse(BaseModel):
    id: str
    email: str
    role: str
    is_2fa_enabled: bool

    model_config = {"from_attributes": True}
