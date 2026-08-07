# System Architecture

## Overview

The URL Shortener Service follows a layered architecture to separate business logic, database operations, and API endpoints.

```
                Client
                   │
                   ▼
            FastAPI Routers
                   │
                   ▼
             Service Layer
                   │
                   ▼
           Repository Layer
                   │
                   ▼
             SQLAlchemy ORM
                   │
                   ▼
              SQLite Database
```

---

## Layers

### API Layer

Responsible for:

- Handling HTTP requests
- Request validation
- Authentication
- Returning HTTP responses

Directory:

```
app/api/
```

---

### Service Layer

Contains all business logic.

Responsibilities:

- User registration
- Authentication
- URL generation
- URL validation
- Dashboard calculations
- Analytics processing

Directory:

```
app/services/
```

---

### Repository Layer

Responsible only for database queries.

Responsibilities:

- CRUD operations
- SQLAlchemy queries
- Database abstraction

Directory:

```
app/repositories/
```

---

### Models

Database entities.

```
User
ShortURL
ClickAnalytics
```

Directory:

```
app/models/
```

---

### Schemas

Pydantic request/response models.

Directory:

```
app/schemas/
```

---

### Core

Application configuration.

Contains:

- Database
- Security
- Config

Directory:

```
app/core/
```

---

## Authentication Flow

```
Register
      │
      ▼
Hash Password
      │
      ▼
Save User
```

```
Login
      │
      ▼
Verify Password
      │
      ▼
Generate JWT
      │
      ▼
Return Access Token
```

---

## URL Flow

```
Create URL
      │
      ▼
Generate Short Code
      │
      ▼
Store Database
      │
      ▼
Return Response
```

---

## Analytics Flow

```
Visit Short URL
        │
        ▼
Increment Click Count
        │
        ▼
Save Click Analytics
        │
        ▼
Redirect User
```

---

## Design Principles

- Separation of Concerns
- Dependency Injection
- Repository Pattern
- Service Layer Pattern
- RESTful APIs
- JWT Authentication