"""
URL Repository

Purpose
-------
Handles all database operations related to the ShortURL model.
"""

from sqlalchemy.orm import Session

from app.models import ShortURL


class URLRepository:
   
    def __init__(self, db: Session):
        self.db = db

   
    # Create Short URL
    
    def create(self, short_url: ShortURL) -> ShortURL:
        
        self.db.add(short_url)
        self.db.commit()
        self.db.refresh(short_url)

        return short_url

   
    # Get URL By ID
    
    def get_by_id(self, url_id: int) -> ShortURL | None:
        """
        Fetch URL using primary key.
        """

        return (
            self.db.query(ShortURL)
            .filter(ShortURL.id == url_id)
            .first()
        )

    
    # Get URL By Short Code
   
    def get_by_short_code(
        self,
        short_code: str,
    ) -> ShortURL | None:

        return (
            self.db.query(ShortURL)
            .filter(ShortURL.short_code == short_code)
            .first()
        )

    
    # Get All URLs Created By User
   
    def get_by_user(
        self,
        user_id: int,
    ) -> list[ShortURL]:
       

        return (
            self.db.query(ShortURL)
            .filter(ShortURL.user_id == user_id)
            .all()
        )

    
    # Update URL
   
    def update(self, short_url: ShortURL) -> ShortURL:
      
        self.db.commit()
        self.db.refresh(short_url)

        return short_url

   
    # Increment Click Count
    
    def increment_click_count(
        self,
        short_url: ShortURL,
    ) -> None:
       

        short_url.click_count += 1

        self.db.commit()

   
    # Delete URL

    def delete(self, short_url: ShortURL) -> None:
        
        self.db.delete(short_url)
        self.db.commit()