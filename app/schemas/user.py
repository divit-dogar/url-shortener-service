from datetime import datetime
import re

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
)



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
# Password Validation

def validate_password_strength(password: str) -> str:
    """
    Validate password strength.

    Rules:
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one number
    - At least one special character
    """

    if len(password) < 8:
        raise ValueError(
            "Password must be at least 8 characters long."
        )

    if not re.search(r"[A-Z]", password):
        raise ValueError(
            "Password must contain at least one uppercase letter."
        )

    if not re.search(r"[a-z]", password):
        raise ValueError(
            "Password must contain at least one lowercase letter."
        )

    if not re.search(r"\d", password):
        raise ValueError(
            "Password must contain at least one number."
        )

    if not re.search(r"[^A-Za-z0-9]", password):
        raise ValueError(
            "Password must contain at least one special character."
        )

    return password


# User Registration Schema

class UserCreate(BaseModel):
    """
    Schema used while creating/registering
    a new user.
    """

    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Full name of the user",
    )

    email: EmailStr

    password: str = Field(
        ...,
        min_length=8,
        description="User password",
    )

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        return validate_password_strength(value)


# User Update Schema

class UserUpdate(BaseModel):
    """
    Schema used while updating user information.
    """

    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )


# User Response Schema

class UserResponse(BaseModel):
    """
    Response returned to the client.

    Password/hashed password is intentionally omitted.
    """

    id: int

    name: str

    email: EmailStr

    is_active: bool

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )