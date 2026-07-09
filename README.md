# AI-First CRM HCP Module

> AI-first CRM module for Healthcare Professionals (HCPs) where interaction records are created and updated exclusively through an AI assistant powered by LangGraph.

---

## Features

- AI-driven interaction logging
- AI-driven interaction editing
- Search Healthcare Professionals
- Retrieve interaction history
- AI-generated follow-up suggestions
- Split-screen CRM interface
- FastAPI REST API
- PostgreSQL persistence
- LangGraph workflow orchestration

---

## Tech Stack

### Frontend

- React
- TypeScript
- Vite
- Redux Toolkit

### Backend

- FastAPI
- Pydantic v2
- SQLAlchemy 2.0
- PostgreSQL

### AI

- LangGraph
- LangChain
- Groq
- llama-3.3-70b-versatile

---

## Project Structure

```text
backend/
database/
docs/
frontend/
README.md
```

---

## Getting Started

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Backend

```bash
cd backend

python -m venv .venv
.venv\Scripts\Activate.ps1

pip install -r requirements.txt

uvicorn app.main:app --reload
```

---

## Database

1. Install PostgreSQL
2. Create database:

```text
ai_first_crm_hcp
```

3. Configure:

```text
backend/.env
```

---

## AI Configuration

```env
GROQ_API_KEY=your_api_key

MODEL_NAME=llama-3.3-70b-versatile
```

> **Note**
>
> The original assignment specifies `gemma2-9b-it`. Since the model has been deprecated by Groq, this project uses `llama-3.3-70b-versatile` while preserving the intended LangGraph architecture.

---

## Documentation

| Document | Description |
|----------|-------------|
| Project Context | Current project state |
| Architecture | System architecture |
| ADR | Architecture decisions |
| Issue Progress | Development roadmap |
| Database Schema | ERD and schema documentation |

---

## API Schemas

Pydantic schemas have been implemented for:

- HealthcareProfessional
- Interaction

Each entity provides:

- Create schema
- Update schema
- Response schema

---

## Backend Architecture

The backend follows a layered architecture to maintain separation of concerns.

```text
FastAPI Routes
        │
        ▼
Pydantic Schemas
        │
        ▼
Service Layer
        │
        ▼
Repository Layer
        │
        ▼
SQLAlchemy ORM Models
        │
        ▼
PostgreSQL
```

Current implementation:

- ✅ SQLAlchemy ORM Models
- ✅ Pydantic Schemas
- ✅ Repository Layer
- ✅ Service Layer

Upcoming:

- ⏳ Service Layer
- ⏳ REST API Endpoints

## Current Progress

### Milestone 1

- ✅ Project Setup

### Milestone 2

- 🚧 Backend Development

### Milestone 3

- ⏳ Frontend Development

### Milestone 4

- ⏳ LangGraph Integration

### Milestone 5

- ⏳ DevOps & Deployment

---

## Verification

Verified components:

- ✅ React + Vite
- ✅ FastAPI
- ✅ PostgreSQL
- ✅ SQLAlchemy ORM Models
- ✅ Pydantic Schemas
- ✅ Repository Layer
- ✅ LangGraph
- ✅ Groq

---

## Database

Current domain model:

- HealthcareProfessional
- Interaction

Implemented:

- SQLAlchemy 2.0 ORM models
- One-to-many relationships
- UUID primary keys
- PostgreSQL JSONB support
- Enumerations
- Repository layer for data access

Documentation:

- `database/schema/schema.md`
- `database/schema/erd.md`
- `database/schema/erd.png`

---

## Development Status

Current Version

- v0.1.0

Completed Backend Layers

- SQLAlchemy ORM Models
- Pydantic Schemas
- Repository Layer

Current Focus

- Service Layer

Next Milestone

- FastAPI REST API

---

## License

Created as part of a technical assessment.