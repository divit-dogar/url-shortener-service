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
        """
        Create a shortened URL.

        The short_code is always auto-generated.
        custom_alias is optional and stored separately.
        """

        # Check custom alias uniqueness
        if url_data.custom_alias:

            existing_alias = (
                self.url_repository.get_by_custom_alias(
                    url_data.custom_alias
                )
            )

            if existing_alias:
                raise ValueError(
                    "Custom alias already exists."
                )

        # Generate short code
        short_code = self._generate_short_code()

        # Ensure generated short code is unique
        print("Dogar",self.url_repository.get_by_short_code(short_code))
        while self.url_repository.get_by_short_code(
            short_code
        ):
            print("while loop eexecuted")
            short_code = self._generate_short_code()

        # Create database object
        short_url = ShortURL(
            original_url=str(url_data.original_url),
            short_code=short_code,
            custom_alias=url_data.custom_alias,
            user_id=user_id,
            expires_at=url_data.expires_at,
            is_active=True,
            click_count=0,
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

        # Update original URL
        if url_data.original_url is not None:
            url.original_url = str(
                url_data.original_url
            )

        # Update custom alias
        if url_data.custom_alias is not None:
            existing_alias = (
                self.url_repository.get_by_custom_alias(
                    url_data.custom_alias
                )
            )

            if (
               existing_alias
                and existing_alias.id != url.id
            ):
                raise ValueError(
                    "Custom alias already exists."
                )

            url.custom_alias = url_data.custom_alias

        # Update expiration date
        if url_data.expires_at is not None:
            url.expires_at = url_data.expires_at

        updated = self.url_repository.update(url)

        return URLResponse.model_validate(updated)
        # Enable URL

    def enable_url(
        self,
        url_id: int,
        user_id: int,
    ) -> URLResponse:

        url = self.url_repository.get_by_id(url_id)

        if not url:
            raise ValueError("URL not found.")

        if url.user_id != user_id:
            raise PermissionError(
                "You are not authorized to enable this URL."
            )

        updated = self.url_repository.enable(url)

        return URLResponse.model_validate(updated)

    # Disable URL

    def disable_url(
        self,
        url_id: int,
        user_id: int,
    ) -> URLResponse:

        url = self.url_repository.get_by_id(url_id)

        if not url:
            raise ValueError("URL not found.")

        if url.user_id != user_id:
            raise PermissionError(
                "You are not authorized to disable this URL."
            )

        updated = self.url_repository.disable(url)

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

    # Increment Click Count

def increment_clicks(
    self,
    short_code: str,
    ip_address: str | None = None,
    user_agent: str | None = None,
    browser: str | None = None,
    operating_system: str | None = None,
    device: str | None = None,
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
        browser=browser,
        operating_system=operating_system,
        device=device,
        referrer=referrer,
    )

    # Notify observers
    self.click_publisher.notify(event)
       