"""
Authentication Schemas

Purpose
-------
Contains schemas used for
authentication and JWT token handling.
"""

from datetime import datetime

from pydantic import BaseModel, EmailStr



# Login Request

class LoginRequest(BaseModel):
    """
    Schema used while logging in.
    """

    email: EmailStr

    password: str



# JWT Token Response

class Token(BaseModel):
    """
    Response returned after
    successful authentication.
    """

    access_token: str

    token_type: str = "bearer"



# JWT Payload

class TokenPayload(BaseModel):
    """
    Data extracted after decoding JWT.
    """

    sub: str

    exp: datetime