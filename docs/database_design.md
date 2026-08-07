# Database Design

## Overview

The application uses SQLite with SQLAlchemy ORM.

There are three main tables:

- users
- short_urls
- click_analytics

---

# users

Stores registered users.

| Column | Type | Description |

| id | Integer | Primary Key |
| name | String | User name |
| email | String | Unique email |
| hashed_password | String | Password hash |
| is_active | Boolean | Active status |
| created_at | DateTime | Created timestamp |
| updated_at | DateTime | Updated timestamp |

Primary Key

```
id
```

Indexes

```
email
```

---

# short_urls

Stores shortened URLs.

| Column | Type | Description |

| id | Integer | Primary Key |
| original_url | Text | Original URL |
| short_code | String | Unique short code |
| user_id | Integer | Owner |
| click_count | Integer | Total clicks |
| expires_at | DateTime | Expiration |
| created_at | DateTime | Created timestamp |
| updated_at | DateTime | Updated timestamp |

Foreign Key

```
user_id
→ users.id
```

Indexes

```
short_code
```

---

# click_analytics

Stores click history.

| Column | Type | Description |

| id | Integer | Primary Key |
| short_url_id | Integer | URL reference |
| ip_address | String | Visitor IP |
| user_agent | String | Browser |
| referrer | String | Referrer |
| clicked_at | DateTime | Click timestamp |

Foreign Key

```
short_url_id
→ short_urls.id
```

---

# Relationships

```
User
│
├── has many
│
▼
ShortURL
│
├── has many
│
▼
ClickAnalytics
```

---

# Entity Relationship Diagram

```

|   Users   |

| id        |
| name      |
| email     |
| password  |

      |
      | 1
      |
      | *

|  Short URLs   |

| id            |
| original_url  |
| short_code    |
| user_id       |
| click_count   |

      |
      | 1
      |
      | *

| Click Analytics  |

| id               |
| short_url_id     |
| ip_address       |
| user_agent       |
| referrer         |
| clicked_at       |

```

---

# Indexes

Current indexes:

- users.email
- short_urls.short_code
- Primary keys

These indexes improve:

- User login performance
- URL lookup speed
- Analytics retrieval