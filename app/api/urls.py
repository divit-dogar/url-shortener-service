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
from fastapi import Request
from fastapi.responses import RedirectResponse
from fastapi.responses import RedirectResponse, StreamingResponse
from app.core.config import settings
from app.services.qr_code_service import QRCodeService

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
    "/{short_code}/qr",
)
def generate_qr_code(
    short_code: str,
    db: Session = Depends(get_db),
):
    """
    Generate a QR code for a shortened URL.
    """

    service = URLService(db)

    try:
        url = service.get_url(short_code)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

    short_url = (
        f"{settings.BASE_URL}/urls/{url.short_code}"
    )

    qr_service = QRCodeService()

    qr_image = qr_service.generate(
        short_url
    )

    return StreamingResponse(
        qr_image,
        media_type="image/png",
        headers={
            "Content-Disposition": (
                f'inline; filename="{url.short_code}.png"'
            )
        },
    )

@router.get(
    "/{short_code}",
)
def get_url(
    short_code: str,
    request: Request,
    db: Session = Depends(get_db),
):
    
    # Retrieve original URL.
    
    service = URLService(db)

    url = service.get_url(short_code)

    service.increment_clicks(
        short_code=short_code,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
        referrer=request.headers.get("referer"),
    )

    return RedirectResponse(
        url=url.original_url,
        status_code=307,
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