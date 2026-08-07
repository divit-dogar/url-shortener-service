# URL Shortener service

A production-ready URL Shortener Service built with **FastAPI**, **SQLAlchemy**, **JWT Authentication**, and **SQLite**.

---

## Features

- User Registration & Login
- JWT Authentication
- OAuth2 Authorization
- URL Shortening
- Custom Short Alias
- URL Expiration
- Click Tracking
- URL Analytics
- Dashboard
- Logging Middleware
- Global Exception Handling
- Alembic Database Migrations
- RESTful APIs
- Swagger Documentation
- Unit Tests

---

## Tech Stack

- Python 3.13
- FastAPI
- SQLAlchemy
- Alembic
- SQLite
- Pydantic
- JWT
- Pytest

---

## Project Structure

```text
app/
│
├── api/
├── core/
├── dependencies/
├── exceptions/
├── middleware/
├── models/
├── repositories/
├── schemas/
├── services/
└── main.py

alembic/
tests/
```

---

## Installation

Clone the repository

```bash
git clone <repository-url>
cd url-shortener-service
```

Create virtual environment

```bash
python -m venv venv
```

Activate virtual environment

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create

```text
.env.development
```

Example

```env
APP_NAME=URL Shortener Service
APP_ENV=development
DEBUG=True

DATABASE_URL=sqlite:///./url_shortener.db

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## Run Server

```bash
uvicorn app.main:app --reload
```

---

## Swagger

```
http://127.0.0.1:8000/docs
```

---

## Running Tests

```bash
pytest
```

---

## Database Migration

Create migration

```bash
alembic revision --autogenerate -m "message"
```

Run migration

```bash
alembic upgrade head
```

---

## API Endpoints

### Authentication

- POST /auth/register
- POST /auth/login

### URLs

- POST /urls
- GET /urls/{short_code}
- PUT /urls/{url_id}
- DELETE /urls/{url_id}

### Analytics

- GET /analytics/{short_code}

### Dashboard

- GET /dashboard

---

## Future Improvements

- Redis Caching
- Rate Limiting
- Docker
- PostgreSQL
- QR Code Generation
- Custom Domain Support

---

## Author

Dayanand