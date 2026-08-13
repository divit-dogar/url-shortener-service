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
    URLListResponse,
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
    RefreshTokenRequest,
    Token,
    TokenPayload,
)

from .auth import (
    ChangePasswordRequest,
    LoginRequest,
    RefreshTokenRequest,
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
    "URLListResponse",
    "URLResponse",
    "URLStats",
    "URLUpdate",

    # Analytics
    "ClickAnalyticsResponse",
    "URLAnalyticsResponse",

    # Auth
    "ChangePasswordRequest",
    "LoginRequest",
    "RefreshTokenRequest",
    "Token",
    "TokenPayload",

    

]