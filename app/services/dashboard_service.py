"""
Dashboard Service

Provides dashboard statistics.
"""

from sqlalchemy.orm import Session

from app.repositories import (
    URLRepository,
    AnalyticsRepository,
)


class DashboardService:

    # Dashboard business logic.

    def __init__(self, db: Session):
        self.url_repository = URLRepository(db)
        self.analytics_repository = AnalyticsRepository(db)

    def get_dashboard(
        self,
        user_id: int,
    ) -> dict:
        
        # Return dashboard statistics.

        urls = self.url_repository.get_by_user(user_id)

        total_urls = len(urls)

        total_clicks = sum(
            url.click_count
            for url in urls
        )

        return {
            "total_urls": total_urls,
            "total_clicks": total_clicks,
            "urls": urls,
        }