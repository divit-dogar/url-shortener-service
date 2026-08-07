from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class ShortURL(Base):
    __tablename__ = "short_urls"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # URL Information
    original_url = Column(Text, nullable=False)

    short_code = Column(
        String(20),
        unique=True,
        index=True,
        nullable=False,
    )

    # Owner
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    # Analytics
    click_count = Column(Integer, default=0)

    expires_at = Column(DateTime(timezone=True), nullable=True)

    # Audit Fields
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Relationship
    owner = relationship(
        "User",
        back_populates="urls",
    )

    clicks = relationship(
    "ClickAnalytics",
    back_populates="short_url",
    cascade="all, delete-orphan",
    )