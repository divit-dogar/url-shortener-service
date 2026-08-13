"""
Authentication Schemas

Purpose
-------
Contains schemas used for
authentication and JWT token handling.
"""

from datetime import datetime

from pydantic import (
    BaseModel,
    EmailStr,
    field_validator
)
from app.schemas.user import validate_password_strength


# Login Request

class LoginRequest(BaseModel):
    """
    Schema used while logging in.
    """

    username: str
    password: str


# JWT Token Response

class Token(BaseModel):
    """
    Response returned after
    successful authentication.
    """

    access_token: str
    refresh_token: str | None = None
    token_type: str = "bearer"


# JWT Payload

class TokenPayload(BaseModel):
    """
    Data extracted after decoding JWT.
    """

    sub: str
    exp: datetime


# Refresh Token Request

class RefreshTokenRequest(BaseModel):
    """
    Request used to refresh an access token.
    """

    refresh_token: str

class ChangePasswordRequest(BaseModel):
    """
    Request used to change the current user's password.
    """

    current_password: str

    new_password: str

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, value: str) -> str:
        return validate_password_strength(value)