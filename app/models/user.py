from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # User Information
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)

    # Authentication
    hashed_password = Column(String(255), nullable=False)

    # Account Status
    is_active = Column(Boolean, default=True)

    # Audit Fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    urls = relationship(
    "ShortURL",
    back_populates="owner",
    cascade="all, delete-orphan",
    )

    refresh_tokens = relationship(
    "RefreshToken",
    back_populates="user",
    cascade="all, delete-orphan",
    )
