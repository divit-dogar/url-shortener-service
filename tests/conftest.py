from fastapi.testclient import TestClient

from app.main import app
from app.core.database import Base, engine

from app import models


# Create database tables for tests
Base.metadata.create_all(bind=engine)


client = TestClient(app)
