# Backend Architecture

## Overview

The backend is implemented using FastAPI and follows a layered architecture.

```text
HTTP Request
      │
      ▼
FastAPI Router
      │
      ▼
Pydantic Schema Validation
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
PostgreSQL
```

---

## Directory Structure

```text
app/
├── api/
├── config/
├── core/
├── db/
├── graph/
├── llm/
├── models/
├── prompts/
├── repositories/
├── services/
└── schemas/
```

---

## Responsibilities

### api/

REST endpoints.

---

### config/

Application configuration.

---

### core/

Shared utilities.

---

### db/

Database configuration.

- Engine
- Session
- Base model

---

### graph/

Current implementation

- Graph State
- Router
- Tool Registry
- Log Interaction Tool
- Edit Interaction Tool

---

### llm/

Groq client.

---

### prompts/

System prompts and prompt templates.

### models/

Contains the SQLAlchemy ORM models that represent the application's core business entities.

Current Models

- HealthcareProfessional
- Interaction

Responsibilities

- Define entity attributes
- Configure relationships
- Apply database constraints
- Map Python objects to PostgreSQL tables
- Define enumerations used by the ORM

### schemas/

Contains Pydantic models responsible for:

- Request validation
- Response serialization
- API data contracts

### repositories/

Contains the data access layer responsible for CRUD operations using SQLAlchemy ORM.

Current repositories:

- HealthcareProfessionalRepository
- InteractionRepository

Responsibilities:

- Create entities
- Retrieve entities
- Update entities
- Delete entities
- Query the database

### services/

Contains the application's business logic layer.

Current Services

- HealthcareProfessionalService
- InteractionService

Responsibilities

- Coordinate repositories
- Apply business rules
- Convert Pydantic schemas to SQLAlchemy models
- Serve FastAPI routes
- Serve LangGraph tools

The service layer is independent of FastAPI and SQLAlchemy sessions, making it reusable across different interfaces.

### api/

Contains the REST API layer implemented using FastAPI.

Responsibilities

- Handle HTTP requests
- Validate request payloads
- Invoke the Service Layer
- Serialize responses
- Return appropriate HTTP status codes

Current Routers

- Healthcare Professional API
- Interaction API
