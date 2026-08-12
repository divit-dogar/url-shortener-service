
"""
Main Application

Entry point of the URL Shortener Service.
"""

from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.urls import router as url_router
from app.api.analytics import router as analytics_router
from app.api.dashboard import router as dashboard_router
from app.exceptions.handlers import register_exception_handlers
from app.middleware.logging import LoggingMiddleware


app = FastAPI(
    title="URL Shortener Service",
    description="A URL shortening service built with FastAPI",
    version="1.0.0",
)


# Register middleware

app.add_middleware(LoggingMiddleware)


# Register exception handlers

register_exception_handlers(app)


# Health Check

@app.get("/")
def root():
    """
    Root endpoint to verify the application is running.
    """

    return {
        "message": "URL Shortener Service is running 🚀"
    }


# Register Routers

app.include_router(auth_router)
app.include_router(url_router)
app.include_router(analytics_router)
app.include_router(dashboard_router)