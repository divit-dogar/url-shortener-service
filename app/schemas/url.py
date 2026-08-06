"""
URL Schemas

Purpose
-------
Contains request and response schemas
related to URL shortening operations.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, HttpUrl



# Create Short URL

class URLCreate(BaseModel):
    """
    Request schema used for creating
    a shortened URL.
    """

    original_url: HttpUrl

    custom_alias: str | None = Field(
        default=None,
        min_length=3,
        max_length=20,
        description="Optional custom short code"
    )

    expires_at: datetime | None = None


# Update URL

class URLUpdate(BaseModel):
    """
    Schema used while updating
    an existing short URL.
    """

    original_url: HttpUrl | None = None

    expires_at: datetime | None = None



# URL Response

class URLResponse(BaseModel):
    """
    Response returned after creating
    or fetching a short URL.
    """

    id: int

    original_url: HttpUrl

    short_code: str

    click_count: int

    expires_at: datetime | None

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# URL Analytics

class URLStats(BaseModel):
    """
    Statistics returned
    for a shortened URL.
    """

    short_code: str

    total_clicks: int

    created_at: datetime

    expires_at: datetime | None