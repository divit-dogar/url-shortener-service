"""
Security Module

Purpose
-------
Handles password hashing, JWT creation,
JWT verification, and OAuth2 authentication.
"""

from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# Password Hashing Configuration
# CryptContext manages password hashing algorithms.
# bcrypt is the industry standard for password hashing.
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

# Password Hashing

def hash_password(password: str) -> str:
    """
    Convert plain password into hashed password.

    Example:
    --------
    divit@123

    becomes

    $2b$12$Jsd83k.....
    """

    return pwd_context.hash(password)

# Password Verification

def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    Compare user entered password
    with stored hashed password.
    """

    return pwd_context.verify(
        plain_password,
        hashed_password,
    )

# Create JWT Access Token

def create_access_token(
    subject: str,
    expires_delta: timedelta | None = None,
) -> str:
    """
    Generate JWT access token.

    Parameters
    ----------
    subject:
        Usually User ID.

    expires_delta:
        Optional expiry duration.
    """

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    payload: dict[str, Any] = {
        "sub": subject,
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

# Decode JWT


def decode_access_token(token: str) -> dict[str, Any]:
    """
    Decode and verify JWT token.
    Raises JWTError if token is invalid.
    """

    return jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
    )