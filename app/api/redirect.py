"""
Redirect API

Handles public short URL redirects.
"""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.url_service import URLService


router = APIRouter(
    tags=["Redirect"],
)


@router.get(
    "/{short_code}",
)
def redirect_short_url(
    short_code: str,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Redirect a short URL to its original URL.
    """

    service = URLService(db)

    try:
        url = service.get_url(short_code)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

    # Check active status
    if not url.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="URL is disabled.",
        )

    # Check expiration
    if (
        url.expires_at is not None
        and url.expires_at <= datetime.now(timezone.utc)
    ):
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="URL has expired.",
        )

    # Record analytics
    service.increment_clicks(
        short_code=short_code,
        ip_address=(
            request.client.host
            if request.client
            else None
        ),
        user_agent=request.headers.get("user-agent"),
        referrer=request.headers.get("referer"),
    )

    return RedirectResponse(
        url=url.original_url,
        status_code=status.HTTP_302_FOUND,
    )