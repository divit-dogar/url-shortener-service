from dataclasses import dataclass


@dataclass
class ClickEvent:
    
    # Represents a click on a shortened URL.

    short_url_id: int
    short_code: str
    ip_address: str | None = None
    user_agent: str | None = None
    referrer: str | None = None