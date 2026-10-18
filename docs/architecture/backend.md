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

Application configuration (`settings.py`).

| Setting | Default | Purpose |
|---------|---------|---------|
| `DATABASE_URL` | — | PostgreSQL connection |
| `GROQ_API_KEY` | — | Groq API key |
| `MODEL_NAME` | `openai/gpt-oss-120b` | LLM model |
| `ROUTER_MODE` | `llm` | `llm` or `keyword` routing |

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
- Router (LLM intent classification with keyword fallback, ADR-004)
- Unsupported tool (no database access)
- Tool Registry
- Tool Execution with error handling
- Log Interaction Tool
- Edit Interaction Tool
- Search Healthcare Professional Tool
- Retrieve Interaction History Tool
- Suggest Follow-up Tool
- Shared date parsing (`tools/dates.py`)
- Shared interaction serialization (`tools/serializers.py`)
- Shared validation (`tools/validation.py`): HCP name resolution, placeholder cleaning, mention checks

---

### llm/

Groq client configuration.

| Item | Value |
|------|-------|
| Model | `openai/gpt-oss-120b` (configured through `MODEL_NAME`) |
| Temperature | 0 |

Provides `structured(schema)`, which binds the LLM to a Pydantic schema using JSON Schema output.

---

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
- AI Chat API

---

## Error Handling

The AI Chat API always returns HTTP 200 with a `ChatResponse`.

| Situation | `tool_output.error_type` | User Message |
|-----------|--------------------------|--------------|
| Incomplete interaction | `validation` | Names the missing field |
| No HCP named | `validation` | "Which Healthcare Professional do you mean?" |
| Edit with nothing to change | `validation` | "I couldn't tell what to change" |
| Greeting, capability question, delete request | `unsupported` | Lists what the assistant can do |
| HCP or interaction not found | `validation` | e.g. "HCP 'X' not found." |
| Unreadable date | `validation` | Asks for a valid date |
| LLM, database or routing failure | `internal` | Generic retry message |

Unexpected errors are logged with their full stack trace on the server and are never returned to the client.

---

## CORS

The API accepts requests from local development origins:

```text
http://localhost:<any port>
http://127.0.0.1:<any port>
```

Vite moves to port 5174+ when 5173 is busy, so a fixed origin list is not used.
