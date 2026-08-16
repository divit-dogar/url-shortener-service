from datetime import date, datetime

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


class DailyClickResponse(BaseModel):
    date: date
    clicks: int


class URLAnalyticsResponse(BaseModel):
    short_code: str
    original_url: str
    total_clicks: int
    unique_visitors: int
    daily_click_count: list[DailyClickResponse]
    last_access_time: datetime | None = None
    click_history: list[ClickAnalyticsResponse]
