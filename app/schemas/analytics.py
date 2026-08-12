from datetime import datetime

from pydantic import BaseModel


class ClickAnalyticsResponse(BaseModel):
    visited_at: datetime
    ip_address: str | None = None
    user_agent: str | None = None
    browser: str | None = None
    operating_system: str | None = None
    device: str | None = None
    referrer: str | None = None

    model_config = {
        "from_attributes": True,
    }


class URLAnalyticsResponse(BaseModel):
    short_code: str
    original_url: str
    total_clicks: int
    click_history: list[ClickAnalyticsResponse]