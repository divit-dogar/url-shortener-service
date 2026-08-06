"""
User Repository

Purpose
-------
Contains all database operations
related to the User model.
"""

from sqlalchemy.orm import Session

from app.models import User


class UserRepository:
    """
    Handles CRUD operations
    for User table.
    """

    def __init__(self, db: Session):
        self.db = db

    
    # Create User
    
    def create(self, user: User) -> User:
        """
        Save new user.
        """

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    
    # Find User By Email
    
    def get_by_email(
        self,
        email: str,
    ) -> User | None:

        return (
            self.db.query(User)
            .filter(User.email == email)
            .first()
        )

    
    # Find User By ID
    
    def get_by_id(
        self,
        user_id: int,
    ) -> User | None:

        return (
            self.db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    
    # Update User
    
    def update(self) -> None:
        """
        Commit pending changes.
        """

        self.db.commit()

    # Delete User

    def delete(
        self,
        user: User,
    ) -> None:

        self.db.delete(user)
        self.db.commit()