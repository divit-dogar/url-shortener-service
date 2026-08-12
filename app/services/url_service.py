"""
URL Service

## Purpose

Contains business logic related
to URL shortening operations.
"""

import secrets

from sqlalchemy.orm import Session

from app.models import ShortURL
from app.repositories import URLRepository
from app.schemas import (
    URLCreate,
    URLResponse,
    URLUpdate,
)
from app.events.analytics_observer import AnalyticsObserver
from app.events.click_event import ClickEvent
from app.events.publisher import ClickEventPublisher


class URLService:
    """
    Handles URL shortening operations.
    """

    def __init__(self, db: Session):
        self.url_repository = URLRepository(db)

        self.click_publisher = ClickEventPublisher()

        self.click_publisher.subscribe(
            AnalyticsObserver(db)
        )

    # Generate Short Code

    def _generate_short_code(
        self,
        length: int = 6,
    ) -> str:
        """
        Generate random URL code.
        """

        return secrets.token_urlsafe(length)[:length]

    # Create Short URL

    def create_url(
        self,
        url_data: URLCreate,
        user_id: int,
    ) -> URLResponse:

        # Use custom alias if provided
        short_code = (
            url_data.custom_alias
            if url_data.custom_alias
            else self._generate_short_code()
        )

        # Check duplicate short code
        if self.url_repository.get_by_short_code(short_code):
            raise ValueError("Short code already exists.")

        # Create database object
        short_url = ShortURL(
            original_url=str(url_data.original_url),
            short_code=short_code,
            user_id=user_id,
            expires_at=url_data.expires_at,
        )

        # Save URL
        url = self.url_repository.create(short_url)

        return URLResponse.model_validate(url)

    # Get URL By Short Code

    def get_url(
        self,
        short_code: str,
    ) -> ShortURL:

        url = self.url_repository.get_by_short_code(
            short_code
        )

        if not url:
            raise ValueError("URL not found.")

        return url

    # Get URL By ID

    def get_url_by_id(
        self,
        url_id: int,
        user_id: int,
    ) -> URLResponse:
        """
        Get URL details by ID.

        Only the owner of the URL can view its details.
        """

        url = self.url_repository.get_by_id(url_id)

        if not url:
            raise ValueError("URL not found.")

        if url.user_id != user_id:
            raise PermissionError(
                "You are not authorized to view this URL."
            )

        return URLResponse.model_validate(url)

    # List URLs

    def list_urls(
        self,
        user_id: int,
        page: int = 1,
        page_size: int = 10,
        search: str | None = None,
        status: str | None = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> tuple[list[URLResponse], int]:

        if page < 1:
            raise ValueError(
                "Page number must be greater than 0."
            )

        if page_size < 1 or page_size > 100:
            raise ValueError(
                "Page size must be between 1 and 100."
            )

        allowed_statuses = {
            "active",
            "disabled",
            "expired",
        }

        if status and status not in allowed_statuses:
            raise ValueError(
                "Status must be active, disabled, or expired."
            )

        allowed_sort_fields = {
            "created_at",
            "click_count",
            "expires_at",
        }

        if sort_by not in allowed_sort_fields:
            raise ValueError(
                "Invalid sort field."
            )

        if sort_order.lower() not in {"asc", "desc"}:
            raise ValueError(
                "Sort order must be asc or desc."
            )

        urls, total = (
            self.url_repository.get_by_user_paginated(
                user_id=user_id,
                page=page,
                page_size=page_size,
                search=search,
                status=status,
                sort_by=sort_by,
                sort_order=sort_order,
            )
        )

        return (
            [
                URLResponse.model_validate(url)
                for url in urls
            ],
            total,
        )

    # Update URL

    def update_url(
        self,
        url_id: int,
        url_data: URLUpdate,
        user_id: int,
    ) -> URLResponse:

        url = self.url_repository.get_by_id(url_id)

        if not url:
            raise ValueError("URL not found.")

        if url.user_id != user_id:
            raise PermissionError(
                "You are not authorized to update this URL."
            )

        if url_data.original_url:
            url.original_url = str(
                url_data.original_url
            )

        if url_data.expires_at:
            url.expires_at = url_data.expires_at

        updated = self.url_repository.update(url)

        return URLResponse.model_validate(updated)

    # Delete URL

    def delete_url(
        self,
        url_id: int,
        user_id: int,
    ) -> None:

        url = self.url_repository.get_by_id(url_id)

        if not url:
            raise ValueError("URL not found.")

        if url.user_id != user_id:
            raise PermissionError(
                "You are not authorized to delete this URL."
            )

        self.url_repository.delete(url)

    # Increment Click Count

    def increment_clicks(
        self,
        short_code: str,
        ip_address: str | None = None,
        user_agent: str | None = None,
        referrer: str | None = None,
    ) -> None:

        url = self.url_repository.get_by_short_code(
            short_code
        )

        if not url:
            raise ValueError("URL not found.")

        # Increment total click count
        self.url_repository.increment_click_count(
            url
        )

        # Create click event
        event = ClickEvent(
            short_url_id=url.id,
            short_code=url.short_code,
            ip_address=ip_address,
            user_agent=user_agent,
            referrer=referrer,
        )

        # Notify observers
        self.click_publisher.notify(event)