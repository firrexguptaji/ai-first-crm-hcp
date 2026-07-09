# Backend Architecture

## Overview

The backend is implemented using FastAPI and follows a layered architecture.

```text
API

↓

Services

↓

Repositories

↓

SQLAlchemy Models

↓

PostgreSQL
```

---

## Directory Structure

```text
app/

api/
config/
core/
db/
graph/
llm/
models/
prompts/
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

LangGraph workflow.

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

