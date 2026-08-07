"""
URL API

Handles URL shortening operations.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies import get_current_user
from app.models import User
from app.schemas import URLCreate, URLResponse, URLUpdate
from app.services.url_service import URLService

router = APIRouter(
    prefix="/urls",
    tags=["URLs"],
)

@router.post(
    "",
    response_model=URLResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_url(
    url: URLCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    
    # Create a shortened URL.

    service = URLService(db)

    try:
        return service.create_url(
            url_data=url,
            user_id=current_user.id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.get(
    "/{short_code}",
)
def get_url(
    short_code: str,
    db: Session = Depends(get_db),
):
    
    # Retrieve original URL.
    
    service = URLService(db)

    try:
        return service.get_url(short_code)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )


@router.put(
    "/{url_id}",
    response_model=URLResponse,
)
def update_url(
    url_id: int,
    url: URLUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    
    # Update an existing short URL.
    
    service = URLService(db)

    try:
        return service.update_url(
            url_id=url_id,
            url_data=url,
            user_id=current_user.id,
        )
    except PermissionError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        )

@router.delete(
    "/{url_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_url(
    url_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    
    # Delete a short URL.

    service = URLService(db)

    try:
        service.delete_url(
            url_id=url_id,
            user_id=current_user.id,
        )
    except PermissionError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        )