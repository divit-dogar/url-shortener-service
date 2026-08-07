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
    ) -> dict:
       
       # Return analytics for a short URL.
        

        url = self.url_repository.get_by_short_code(
            short_code
        )

        if not url:
            raise ValueError(
                "URL not found."
            )

        total_clicks = (
            self.analytics_repository.get_total_clicks(
                url.id
            )
        )

        click_history = (
            self.analytics_repository.get_by_short_url(
                url.id
            )
        )

        return {
            "short_code": url.short_code,
            "original_url": url.original_url,
            "total_clicks": total_clicks,
            "click_history": click_history,
        }