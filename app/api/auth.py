"""
Authentication API

Handles user registration,
login, and token refresh.
"""

from fastapi import APIRouter, Depends, Form, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas import (
    ChangePasswordRequest,
    RefreshTokenRequest,
    LoginRequest,
    Token,
    UserCreate,
    UserResponse,
)

from app.dependencies import get_current_user
from app.models import User
from app.services.auth_service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


# --------------------------------------------------
# User Registration
# --------------------------------------------------

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    """
    Register a new user.
    """

    service = AuthService(db)

    try:
        return service.register(user)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


# --------------------------------------------------
# Login
# --------------------------------------------------
@router.post(
    "/login",
    response_model=Token,
)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db),
):
    service = AuthService(db)

    try:
        return service.login(
            username=data.username,
            password=data.password,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        )
# --------------------------------------------------
# Refresh Token
# --------------------------------------------------

@router.post(
    "/refresh",
    response_model=Token,
)
def refresh_token(
    data: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    """
    Generate a new access token
    using a valid refresh token.
    """

    service = AuthService(db)

    try:
        return service.refresh_access_token(
            data.refresh_token
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        )

@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
)
def logout(
    data: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    """
    Revoke a refresh token and log the user out.
    """

    service = AuthService(db)

    try:
        service.logout(data.refresh_token)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        )
    
@router.post(
    "/change-password",
    status_code=status.HTTP_204_NO_CONTENT,
)
def change_password(
    data: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Change the password of the authenticated user.
    """

    service = AuthService(db)

    try:
        service.change_password(
            user_id=current_user.id,
            data=data,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )