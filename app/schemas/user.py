
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ==========================================================
# User Registration Schema
# ==========================================================
class UserCreate(BaseModel):
    """
    Schema used while creating/registering a new user.

    This schema validates the incoming request body.
    """

    # User's full name
    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Full name of the user"
    )

    # Automatically validates email format
    email: EmailStr

    # Password received from client.
    # NOTE:
    # Password will NEVER be stored directly.
    # It will be hashed inside the service layer.
    password: str = Field(
        ...,
        min_length=8,
        description="User password"
    )


# ==========================================================
# User Update Schema
# ==========================================================
class UserUpdate(BaseModel):
    """
    Schema used while updating user information.

    All fields are optional because
    the user may update only one field.
    """

    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )


# ==========================================================
# User Response Schema
# ==========================================================
class UserResponse(BaseModel):
    """
    Schema returned to the client.

    IMPORTANT:
    Password/Hashed Password is intentionally omitted.
    """

    id: int

    name: str

    email: EmailStr

    is_active: bool

    created_at: datetime

    # Allows conversion from SQLAlchemy Model
    # to Pydantic Schema.
    model_config = ConfigDict(
        from_attributes=True
    )