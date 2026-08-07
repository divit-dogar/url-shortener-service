# API Design

## Base URL

```
http://localhost:8000
```

---

# Authentication

Authentication uses JWT Bearer Tokens.

Workflow:

```
Register
      │
      ▼
Login
      │
      ▼
Receive JWT
      │
      ▼
Authorize
      │
      ▼
Access Protected APIs
```

---

# Authentication APIs

## Register

```
POST /auth/register
```

### Request

```json
{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "Password@123"
}
```

### Response

```json
{
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com"
}
```

Status Codes

- 201 Created
- 400 Bad Request

---

## Login

```
POST /auth/login
```

### Request

```
username=john@example.com
password=Password@123
```

### Response

```json
{
    "access_token": "...",
    "token_type": "bearer"
}
```

Status Codes

- 200 OK
- 401 Unauthorized

---

# URL APIs

Requires JWT Authentication.

---

## Create Short URL

```
POST /urls
```

Headers

```
Authorization: Bearer <token>
```

Request

```json
{
    "original_url": "https://google.com",
    "custom_alias": "google",
    "expires_at": null
}
```

Response

```json
{
    "id": 1,
    "short_code": "google",
    "original_url": "https://google.com"
}
```

Status Codes

- 201 Created
- 400 Bad Request
- 401 Unauthorized

---

## Redirect URL

```
GET /urls/{short_code}
```

Example

```
GET /urls/google
```

Behavior

- Finds URL
- Records click
- Increments click count
- Redirects to original URL

Response

```
307 Temporary Redirect
```

---

## Update URL

```
PUT /urls/{url_id}
```

Requires ownership of the URL.

Status Codes

- 200 OK
- 401 Unauthorized
- 404 Not Found

---

## Delete URL

```
DELETE /urls/{url_id}
```

Requires ownership of the URL.

Status Codes

- 204 No Content
- 401 Unauthorized
- 404 Not Found

---

# Analytics APIs

Requires JWT Authentication.

## Get URL Analytics

```
GET /analytics/{short_code}
```

Response

```json
{
    "short_code": "google",
    "original_url": "https://google.com",
    "total_clicks": 15,
    "click_history": [
        {
            "clicked_at": "...",
            "ip_address": "...",
            "user_agent": "..."
        }
    ]
}
```

Status Codes

- 200 OK
- 401 Unauthorized
- 404 Not Found

---

# Dashboard APIs

Requires JWT Authentication.

## Dashboard

```
GET /dashboard
```

Returns summary information for the authenticated user.

Example Response

```json
{
    "total_urls": 12,
    "total_clicks": 154,
    "active_urls": 10,
    "expired_urls": 2
}
```

Status Codes

- 200 OK
- 401 Unauthorized

---

# Security

The application uses:

- JWT Authentication
- OAuth2 Password Flow
- Password Hashing
- Protected Endpoints
- Authorization Checks

---

# Error Responses

Example

```json
{
    "detail": "Invalid credentials."
}
```

Common HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 204 | Deleted |
| 400 | Bad Request |
| 401 | Unauthorized |
| 404 | Not Found |
| 500 | Internal Server Error |