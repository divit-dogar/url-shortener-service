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
            .order_by(
                ClickAnalytics.visited_at.desc()
            )
            .all()
        )

    # Get Total Clicks

    def get_total_clicks(
        self,
        short_url_id: int,
    ) -> int:

        return (
            self.db.query(
                func.count(ClickAnalytics.id)
            )
            .filter(
                ClickAnalytics.short_url_id == short_url_id
            )
            .scalar()
            or 0
        )

    # Get Unique Visitors

    def get_unique_visitors(
        self,
        short_url_id: int,
    ) -> int:

        return (
            self.db.query(
                func.count(
                    func.distinct(
                        ClickAnalytics.ip_address
                    )
                )
            )
            .filter(
                ClickAnalytics.short_url_id == short_url_id
            )
            .scalar()
            or 0
        )

    # Get Daily Click Count

    def get_daily_click_count(
        self,
        short_url_id: int,
    ) -> list[dict]:

        results = (
            self.db.query(
                func.date(
                    ClickAnalytics.visited_at
                ).label("date"),
                func.count(
                    ClickAnalytics.id
                ).label("clicks"),
            )
            .filter(
                ClickAnalytics.short_url_id == short_url_id
            )
            .group_by(
                func.date(
                    ClickAnalytics.visited_at
                )
            )
            .order_by(
                func.date(
                    ClickAnalytics.visited_at
                )
            )
            .all()
        )

        return [
            {
                "date": row.date,
                "clicks": row.clicks,
            }
            for row in results
        ]

    # Get Last Access Time

    def get_last_access_time(
        self,
        short_url_id: int,
    ):

        return (
            self.db.query(
                func.max(
                    ClickAnalytics.visited_at
                )
            )
            .filter(
                ClickAnalytics.short_url_id == short_url_id
            )
            .scalar()
        )

    # Delete Analytics

    def delete(
        self,
        click: ClickAnalytics,
    ) -> None:

        self.db.delete(click)
        self.db.commit()

  