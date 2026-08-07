"""
URL Service

Purpose
-------
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


class URLService:
    """
    Handles URL shortening operations.
    """

    def __init__(self, db: Session):
        self.url_repository = URLRepository(db)

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

    # Get URL
    
    def get_url(
        self,
        short_code: str,
    ) -> ShortURL:

        url = self.url_repository.get_by_short_code(short_code)

        if not url:
            raise ValueError("URL not found.")

        return url

    # Update URL
    def update_url(
        self,
        url_id: int,
        url_data: URLUpdate,
    ) -> URLResponse:

        url = self.url_repository.get_by_id(url_id)

        if not url:
            raise ValueError("URL not found.")

        if url_data.original_url:
            url.original_url = str(url_data.original_url)

        if url_data.expires_at:
            url.expires_at = url_data.expires_at

        updated = self.url_repository.update(url)

        return URLResponse.model_validate(updated)

   
    # Delete URL
    def delete_url(
        self,
        url_id: int,
    ) -> None:

        url = self.url_repository.get_by_id(url_id)

        if not url:
            raise ValueError("URL not found.")

        self.url_repository.delete(url)

    # Increment Click Count
    
    def increment_clicks(
        self,
        short_code: str,
    ) -> None:

        url = self.url_repository.get_by_short_code(short_code)

        if not url:
            raise ValueError("URL not found.")

        self.url_repository.increment_click_count(url)