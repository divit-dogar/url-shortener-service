from sqlalchemy.orm import Session

from app.events.click_event import ClickEvent
from app.events.observer import ClickObserver
from app.models import ClickAnalytics
from app.repositories import AnalyticsRepository


class AnalyticsObserver(ClickObserver):
    
    # Stores click events in the analytics database.
    
    def __init__(self, db: Session):
        self.analytics_repository = AnalyticsRepository(db)

    def update(self, event: ClickEvent) -> None:

        click = ClickAnalytics(
            short_url_id=event.short_url_id,
            ip_address=event.ip_address,
            user_agent=event.user_agent,
            referrer=event.referrer,
        )

        self.analytics_repository.create(click)