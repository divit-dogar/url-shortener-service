"""
Authentication Service

Purpose
-------
Contains business logic related to
user registration and authentication.
"""

from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models import User
from app.repositories import UserRepository
from app.schemas import (
    LoginRequest,
    Token,
    UserCreate,
    UserResponse,
)


class AuthService:
    """
    Handles user registration
    and login.
    """

    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)

    # Register User
    
    def register(
        self,
        user_data: UserCreate,
    ) -> UserResponse:

        # Check duplicate email
        existing_user = self.user_repository.get_by_email(
            user_data.email
        )

        if existing_user:
            raise ValueError(
                "User already exists."
            )

        # Hash password
        hashed_password = hash_password(
            user_data.password
        )

        # Create database object
        db_user = User(
            name=user_data.name,
            email=user_data.email,
            hashed_password=hashed_password,
        )

        # Save user
        user = self.user_repository.create(
            db_user
        )

        return UserResponse.model_validate(
            user
        )

   
    # Authenticate User
    
    def login(
        self,
        login_data: LoginRequest,
    ) -> Token:

        user = self.user_repository.get_by_email(
            login_data.email
        )

        if user is None:
            raise ValueError(
                "Invalid credentials."
            )

        if not verify_password(
            login_data.password,
            user.hashed_password,
        ):
            raise ValueError(
                "Invalid credentials."
            )

        access_token = create_access_token(
            subject=str(user.id)
        )

        return Token(
            access_token=access_token
        )