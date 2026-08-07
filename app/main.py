
"""
Main Application

Entry point of the URL Shortener Service.
"""

from fastapi import FastAPI
import app.models
from app.core.database import Base, engine
from app.api.auth import router as auth_router
from app.api.urls import router as url_router
from app.api.analytics import router as analytics_router
from app.api.dashboard import router as dashboard_router

## Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI application
app = FastAPI(
    title="URL Shortener Service",
    description="A URL shortening service built with FastAPI",
    version="1.0.0",
)

# Health Check
@app.get("/")
def root():
   # Root endpoint to verify the application is running.
  
    return {
        "message": "URL Shortener Service is running 🚀"
    }

# Register Routers
app.include_router(auth_router)


# Create FastAPI application
app = FastAPI(
    title="URL Shortener Service",
    description="A URL shortening service built with FastAPI",
    version="1.0.0",
)

# Health Check
@app.get("/")
def root():
    
    # Root endpoint to verify the application is running.
    
    return {
        "message": "URL Shortener Service is running 🚀"
    }

# Register Routers

app.include_router(auth_router)
app.include_router(url_router)
app.include_router(analytics_router)
app.include_router(dashboard_router)