from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class ClickAnalytics(Base):
    __tablename__ = "click_analytics"

    # Primary Key
    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    # URL Relationship
    short_url_id = Column(
        Integer,
        ForeignKey("short_urls.id"),
        nullable=False,
    )

    # Visitor Information
    ip_address = Column(
        String(100),
        nullable=True,
    )

    user_agent = Column(
        String(500),
        nullable=True,
    )

    browser = Column(
        String(100),
        nullable=True,
    )

    operating_system = Column(
        String(100),
        nullable=True,
    )

    device = Column(
        String(100),
        nullable=True,
    )

    referrer = Column(
        String(500),
        nullable=True,
    )

    # Visit Timestamp
    visited_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    # Relationship
    short_url = relationship(
        "ShortURL",
        back_populates="clicks",
    )