"""
Main Application

Entry point of the URL Shortener Service.
"""

from fastapi import FastAPI

from app.api.auth import router as auth_router

# Create FastAPI application
app = FastAPI(
    title="URL Shortener Service",
    description="A URL shortening service built with FastAPI",
    version="1.0.0",
)

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