# Backend Architecture

## Overview

The backend is implemented using FastAPI and follows a layered architecture.

```text
API
│
▼
Services
│
▼
Repositories
│
▼
Database
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