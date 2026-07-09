# Database Architecture

## Overview

PostgreSQL is used as the primary relational database.

SQLAlchemy provides ORM support.

---

## Planned Entities

- Healthcare Professional
- Interaction

---

## Database Access

```text
FastAPI

↓

Service Layer

↓

Repository Layer

↓

SQLAlchemy

↓

PostgreSQL
```

---

## Current Status

- PostgreSQL configured
- SQLAlchemy configured
- Database connection verified

The database schema will be implemented in a future milestone.