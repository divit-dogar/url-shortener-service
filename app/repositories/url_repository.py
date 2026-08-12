"""

URL Repository

Handles all database operations related to the ShortURL model.

"""
from sqlalchemy.orm import Session

from app.models import ShortURL


class URLRepository:

    def __init__(self, db: Session):
        self.db = db

    # Create Short URL

    def create(self, short_url: ShortURL) -> ShortURL:
        self.db.add(short_url)
        self.db.commit()
        self.db.refresh(short_url)

        return short_url

    # Get URL By ID

    def get_by_id(self, url_id: int) -> ShortURL | None:
        return (
            self.db.query(ShortURL)
            .filter(ShortURL.id == url_id)
            .first()
        )

    # Get URL By Short Code

    def get_by_short_code(
        self,
        short_code: str,
    ) -> ShortURL | None:

        return (
            self.db.query(ShortURL)
            .filter(ShortURL.short_code == short_code)
            .first()
        )

    # Get URL By Custom Alias

    def get_by_custom_alias(
        self,
        custom_alias: str,
    ) -> ShortURL | None:

        return (
            self.db.query(ShortURL)
            .filter(
                ShortURL.custom_alias == custom_alias
            )
            .first()
        )

    # Get All URLs Created By User

    def get_by_user(
        self,
        user_id: int,
    ) -> list[ShortURL]:

        return (
            self.db.query(ShortURL)
            .filter(ShortURL.user_id == user_id)
            .all()
        )

    # Get URLs with Search / Filter / Sort / Pagination

    def get_by_user_paginated(
        self,
        user_id: int,
        page: int = 1,
        page_size: int = 10,
        search: str | None = None,
        status: str | None = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> tuple[list[ShortURL], int]:

        query = (
            self.db.query(ShortURL)
            .filter(ShortURL.user_id == user_id)
        )

        # Search
        if search:
            search_pattern = f"%{search}%"

            query = query.filter(
                (ShortURL.original_url.ilike(search_pattern))
                | (ShortURL.short_code.ilike(search_pattern))
                | (ShortURL.custom_alias.ilike(search_pattern))
            )

        # Status filter
        if status == "active":
            query = query.filter(ShortURL.is_active.is_(True))

        elif status == "disabled":
            query = query.filter(ShortURL.is_active.is_(False))

        elif status == "expired":
            from datetime import datetime, timezone

            now = datetime.now(timezone.utc)

            query = query.filter(
                ShortURL.expires_at.is_not(None),
                ShortURL.expires_at < now,
            )

        # Total count before pagination
        total = query.count()

        # Sorting
        sort_column = {
            "created_at": ShortURL.created_at,
            "click_count": ShortURL.click_count,
            "expires_at": ShortURL.expires_at,
        }.get(sort_by, ShortURL.created_at)

        if sort_order.lower() == "asc":
            query = query.order_by(sort_column.asc())
        else:
            query = query.order_by(sort_column.desc())

        # Pagination
        offset = (page - 1) * page_size

        urls = (
            query
            .offset(offset)
            .limit(page_size)
            .all()
        )

        return urls, total

    # Update URL

    def update(self, short_url: ShortURL) -> ShortURL:
        self.db.commit()
        self.db.refresh(short_url)

        return short_url

    # Increment Click Count

    def increment_click_count(
        self,
        short_url: ShortURL,
    ) -> None:

        short_url.click_count += 1

        self.db.commit()

    # Enable URL

    def enable(self, short_url: ShortURL) -> ShortURL:
        short_url.is_active = True

        self.db.commit()
        self.db.refresh(short_url)

        return short_url


    # Disable URL

    def disable(self, short_url: ShortURL) -> ShortURL:
        short_url.is_active = False

        self.db.commit()
        self.db.refresh(short_url)

        return short_url

    # Delete URL

    def delete(self, short_url: ShortURL) -> None:
        self.db.delete(short_url)
        self.db.commit()