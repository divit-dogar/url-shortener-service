"""
Analytics Repository

Purpose
-------
Handles all database operations related
to ClickAnalytics.
"""

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import ClickAnalytics


class AnalyticsRepository:
    """
    Repository for click analytics operations.
    """

    def __init__(self, db: Session):
        self.db = db

    # Save Click
   
    def create(
        self,
        click: ClickAnalytics,
    ) -> ClickAnalytics:
        """
        Save click information.
        """

        self.db.add(click)
        self.db.commit()
        self.db.refresh(click)

        return click

    # Get Click History
  
    def get_by_short_url(
        self,
        short_url_id: int,
    ) -> list[ClickAnalytics]:

        return (
            self.db.query(ClickAnalytics)
            .filter(
                ClickAnalytics.short_url_id == short_url_id
            )
            .all()
        )

    # Get Total Clicks
  
    def get_total_clicks(
        self,
        short_url_id: int,
    ) -> int:
        
        return (
            self.db.query(func.count(ClickAnalytics.id))
            .filter(
                ClickAnalytics.short_url_id == short_url_id
            )
            .scalar()
            or 0
        )

    # Delete Analytics

    def delete(
        self,
        click: ClickAnalytics,
    ) -> None:

        self.db.delete(click)
        self.db.commit()