"""
Redirect API

Handles public short URL redirects.
"""

import re
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.url_service import URLService


router = APIRouter(
    tags=["Redirect"],
)


def get_browser(user_agent: str | None) -> str:
    """
    Detect browser from User-Agent.
    """

    if not user_agent:
        return "Unknown"

    user_agent_lower = user_agent.lower()

    # Edge must be checked before Chrome
    if "edg/" in user_agent_lower:
        return "Edge"

    if "opr/" in user_agent_lower or "opera" in user_agent_lower:
        return "Opera"

    if "chrome/" in user_agent_lower:
        return "Chrome"

    if "firefox/" in user_agent_lower:
        return "Firefox"

    if "safari/" in user_agent_lower:
        return "Safari"

    if "msie" in user_agent_lower or "trident/" in user_agent_lower:
        return "Internet Explorer"

    return "Unknown"


def get_operating_system(user_agent: str | None) -> str:
    """
    Detect operating system from User-Agent.
    """

    if not user_agent:
        return "Unknown"

    user_agent_lower = user_agent.lower()

    if "windows" in user_agent_lower:
        return "Windows"

    if "android" in user_agent_lower:
        return "Android"

    if "iphone" in user_agent_lower or "ipad" in user_agent_lower:
        return "iOS"

    if "mac os x" in user_agent_lower or "macintosh" in user_agent_lower:
        return "macOS"

    if "linux" in user_agent_lower:
        return "Linux"

    return "Unknown"


def get_device_type(user_agent: str | None) -> str:
    """
    Detect device type from User-Agent.
    """

    if not user_agent:
        return "Unknown"

    user_agent_lower = user_agent.lower()

    # Tablet
    if "ipad" in user_agent_lower:
        return "Tablet"

    if "tablet" in user_agent_lower:
        return "Tablet"

    # Mobile
    mobile_keywords = [
        "mobile",
        "iphone",
        "android",
        "ipod",
        "blackberry",
        "windows phone",
    ]

    if any(
        keyword in user_agent_lower
        for keyword in mobile_keywords
    ):
        return "Mobile"

    return "Desktop"


@router.get(
    "/{short_code}",
)
def redirect_short_url(
    short_code: str,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Redirect a short URL to its original URL
    and record analytics information.
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
    if url.expires_at is not None:
        expires_at = url.expires_at

        # SQLite may return naive datetime
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(
                tzinfo=timezone.utc
            )

        if expires_at <= datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_410_GONE,
                detail="URL has expired.",
            )

    # Get request information
    user_agent = request.headers.get("user-agent")

    ip_address = (
        request.client.host
        if request.client
        else None
    )

    referrer = request.headers.get("referer")

    # Detect browser, operating system and device
    browser = get_browser(user_agent)

    operating_system = get_operating_system(
        user_agent
    )

    device = get_device_type(user_agent)

    # Record analytics
    service.increment_clicks(
        short_code=short_code,
        ip_address=ip_address,
        user_agent=user_agent,
        browser=browser,
        operating_system=operating_system,
        device=device,
        referrer=referrer,
    )

    return RedirectResponse(
        url=url.original_url,
        status_code=status.HTTP_302_FOUND,
    )