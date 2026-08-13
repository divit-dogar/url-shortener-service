"""
Authentication Service

Purpose
-------
Contains business logic related to
user registration and authentication.
"""

from datetime import datetime, timedelta, timezone

from app.schemas import (
    ChangePasswordRequest,
    Token,
    UserCreate,
    UserResponse,
)
from jose import JWTError
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_access_token,
    hash_password,
    verify_password,
)
from app.models import RefreshToken, User
from app.repositories import UserRepository


class AuthService:
    """
    Handles user registration,
    login, and token refresh.
    """

    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)

    # Register User

    def register(
        self,
        user_data: UserCreate,
    ) -> UserResponse:

        existing_user = (
            self.user_repository.get_by_email(
                user_data.email
            )
        )

        if existing_user:
            raise ValueError(
                "User already exists."
            )

        hashed_password = hash_password(
            user_data.password
        )

        db_user = User(
            name=user_data.name,
            email=user_data.email,
            hashed_password=hashed_password,
        )

        user = self.user_repository.create(
            db_user
        )

        return UserResponse.model_validate(
            user
        )

    # Authenticate User

    def login(
        self,
        username: str,
        password: str,
    ) -> Token:
        """
        Authenticate user and generate
        access and refresh tokens.
        """

        user = self.user_repository.get_by_email(
        username
        )

        if user is None:
            raise ValueError(
                "Invalid credentials."
        )

        if not user.is_active:
            raise ValueError(
                "User account is inactive."
        )

        if not verify_password(
            password,
            user.hashed_password,
        ):
            raise ValueError(
                "Invalid credentials."
            )

        # Create access token
        access_token = create_access_token(
            subject=str(user.id)
        )

        # Create refresh token
        refresh_token = create_refresh_token(
            subject=str(user.id)
        )

        # Calculate refresh token expiry
        expires_at = (
            datetime.now(timezone.utc)
            + timedelta(
                days=settings.REFRESH_TOKEN_EXPIRE_DAYS
            )
        )

        # Store refresh token
        db_refresh_token = RefreshToken(
            user_id=user.id,
            token=refresh_token,
            expires_at=expires_at,
        )

        self.user_repository.db.add(
            db_refresh_token
        )

        self.user_repository.db.commit()

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
        )

    # Refresh Access Token

    def refresh_access_token(
        self,
        refresh_token: str,
    ) -> Token:
        """
        Generate a new access token using
        a valid refresh token.
        """

        try:
            payload = decode_access_token(
                refresh_token
            )

        except JWTError:
            raise ValueError(
                "Invalid or expired refresh token."
            )

        # Make sure this is a refresh token
        if payload.get("type") != "refresh":
            raise ValueError(
                "Invalid refresh token."
            )

        user_id = payload.get("sub")

        if not user_id:
            raise ValueError(
                "Invalid refresh token."
            )

        # Find refresh token in database
        stored_token = (
            self.user_repository.db.query(
                RefreshToken
            )
            .filter(
                RefreshToken.token
                == refresh_token
            )
            .first()
        )

        if not stored_token:
            raise ValueError(
                "Refresh token not found."
            )

        # Check revocation
        if stored_token.revoked_at is not None:
            raise ValueError(
                "Refresh token has been revoked."
            )

        # Check database expiry
        now = datetime.now(timezone.utc)

        expires_at = stored_token.expires_at

        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)

        if expires_at <= now:
            raise ValueError(
            "Refresh token has expired."
        )

        # Find user
        user = self.user_repository.get_by_id(
            int(user_id)
        )

        if not user:
            raise ValueError(
                "User not found."
            )

        if not user.is_active:
            raise ValueError(
                "User account is inactive."
            )

        # Create new access token
        access_token = create_access_token(
            subject=str(user.id)
        )

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
        )
    def logout(
        self,
        refresh_token: str,
    ) -> None:
        """
        Revoke a refresh token.
        """

        stored_token = (
            self.user_repository.db.query(RefreshToken)
            .filter(
                RefreshToken.token == refresh_token
            )
            .first()
        )

        if not stored_token:
            raise ValueError(
                "Refresh token not found."
            )

        if stored_token.revoked_at is not None:
            raise ValueError(
                "Refresh token already revoked."
         )

        stored_token.revoked_at = datetime.now(timezone.utc)

        self.user_repository.db.commit()


    def change_password(
        self,
        user_id: int,
        data: ChangePasswordRequest,
    ) -> None:
        """
        Change the password of the authenticated user.
        """

        user = self.user_repository.get_by_id(user_id)

        if not user:
            raise ValueError(
                "User not found."
            )

        # Verify current password
        if not verify_password(
            data.current_password,
            user.hashed_password,
        ):
            raise ValueError(
                "Current password is incorrect."
            )

        # Prevent using the same password
        if verify_password(
            data.new_password,
            user.hashed_password,
        ):
            raise ValueError(
                "New password must be different from current password."
            )

        # Hash and update password
        user.hashed_password = hash_password(
            data.new_password
        )

        # Revoke all existing refresh tokens
        now = datetime.now(timezone.utc)

        (
            self.user_repository.db.query(RefreshToken)
            .filter(
                RefreshToken.user_id == user_id,
                RefreshToken.revoked_at.is_(None),
            )
            .update(
                {
                    RefreshToken.revoked_at: now
                },
                synchronize_session=False,
            )
        )

        self.user_repository.db.commit()