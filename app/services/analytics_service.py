"""
Analytics Service

Purpose
-------
Contains business logic for
URL analytics.
"""

from sqlalchemy.orm import Session

from app.repositories import (
    AnalyticsRepository,
    URLRepository,
)


class AnalyticsService:
    
    #Handles analytics operations.
    

    def __init__(self, db: Session):
        self.analytics_repository = AnalyticsRepository(db)
        self.url_repository = URLRepository(db)

   
    # Get URL Analytics
    
    def get_url_analytics(
        self,
        short_code: str,
        user_id: int,
    ) -> dict:

        # Get URL
        url = self.url_repository.get_by_short_code(
            short_code
        )

        if not url:
            raise ValueError(
                "URL not found."
            )

        # Check ownership
        if url.user_id != user_id:
            raise PermissionError(
                "You are not authorized to view this analytics."
            )

        # Total clicks
        total_clicks = (
            self.analytics_repository.get_total_clicks(
                url.id
            )
        )

        # Unique visitors
        unique_visitors = (
            self.analytics_repository.get_unique_visitors(
                url.id
            )
        )

        # Daily click count
        daily_click_count = (
            self.analytics_repository.get_daily_click_count(
                url.id
            )
        )

        # Last access time
        last_access_time = (
            self.analytics_repository.get_last_access_time(
                url.id
            )
        )

        # Click history
        click_history = (
            self.analytics_repository.get_by_short_url(
                url.id
            )
        )

        return {
            "short_code": url.short_code,
            "original_url": url.original_url,
            "total_clicks": total_clicks,
            "unique_visitors": unique_visitors,
            "daily_click_count": daily_click_count,
            "last_access_time": last_access_time,
            "click_history": click_history,
        }
    
    