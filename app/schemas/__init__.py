"""
Schema Package

Exports all schemas used across the application.
"""

# User Schemas
from .user import (
    UserCreate,
    UserResponse,
    UserUpdate,
)

# URL Schemas
from .url import (
    URLCreate,
    URLResponse,
    URLStats,
    URLUpdate,
)
from .analytics import (
    ClickAnalyticsResponse,
    URLAnalyticsResponse,
)

# Authentication Schemas
from .auth import (
    LoginRequest,
    Token,
    TokenPayload,
)

__all__ = [
    # User
    "UserCreate",
    "UserResponse",
    "UserUpdate",

    # URL
    "URLCreate",
    "URLResponse",
    "URLStats",
    "URLUpdate",

    # Auth
    "LoginRequest",
    "Token",
    "TokenPayload",
]