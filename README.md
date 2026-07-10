# AI-First CRM HCP Module

> AI-first CRM module for Healthcare Professionals (HCPs) where interaction records are created and updated exclusively through an AI assistant powered by LangGraph.

---

## Features

- AI-powered chat interface through LangGraph
- AI-driven interaction logging
- AI-driven interaction editing
- Healthcare Professional search
- Retrieve interaction history
- AI-generated follow-up recommendations
- FastAPI REST API
- PostgreSQL persistence
- LangGraph workflow orchestration
- End-to-end AI workflow validation
- Responsive split-screen application layout
- Reusable frontend layout components
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

The backend follows a layered architecture with LangGraph orchestrating AI workflows.

```text
                User
                  │
                  ▼
             POST /chat
                  │
                  ▼
              FastAPI API
                  │
                  ▼
             LangGraph Router
                  │
                  ▼
          Selected AI Tool
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

Implemented:

- ✅ SQLAlchemy ORM Models
- ✅ Pydantic Schemas
- ✅ Repository Layer
- ✅ Service Layer
- ✅ REST API
- ✅ LangGraph Integration
- ✅ AI Chat Endpoint
---

## AI Chat Endpoint

The application exposes a LangGraph-powered chat endpoint.

### Endpoint

```http
POST /chat
```

### Request

```json
{
  "message": "Find Alice Brown"
}
```

### Response

```json
{
  "response": "Found 7 Healthcare Professional(s).",
  "tool_name": "search_hcp",
  "tool_output": {
    "success": true,
    "count": 7,
    "results": []
  }
}
```

The endpoint automatically routes user requests to the appropriate LangGraph tool.
---

## Current Progress

### Milestone 1

- ✅ Project Setup

### Milestone 2

- ✅ Backend Development

### Milestone 3

- 🚧 Frontend Development

Completed:

- ✅ Application Layout
- ✅ Redux Toolkit Configuration

Current

- Configure Interaction Details Form

### Milestone 4

- ✅ LangGraph Integration

### Milestone 5

- ⏳ DevOps & Deployment
---

## Verification

Validated components:

- ✅ FastAPI
- ✅ PostgreSQL
- ✅ SQLAlchemy ORM Models
- ✅ Repository Layer
- ✅ Service Layer
- ✅ REST API
- ✅ LangGraph Router
- ✅ Tool Registry
- ✅ AI Chat Endpoint

Validated AI Tools:

- ✅ Log Interaction
- ✅ Edit Interaction
- ✅ Search HCP
- ✅ Retrieve Interaction History
- ✅ Suggest Follow-up
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
## Verification

Validated components:

- ✅ FastAPI
- ✅ PostgreSQL
- ✅ SQLAlchemy ORM Models
- ✅ Repository Layer
- ✅ Service Layer
- ✅ REST API
- ✅ LangGraph Router
- ✅ Tool Registry
- ✅ AI Chat Endpoint

Validated AI Tools:

- ✅ Log Interaction
- ✅ Edit Interaction
- ✅ Search HCP
- ✅ Retrieve Interaction History
- ✅ Suggest Follow-up
--- 

## REST API

### Healthcare Professionals

- POST `/hcps`
- GET `/hcps`
- GET `/hcps/{hcp_id}`
- PUT `/hcps/{hcp_id}`
- DELETE `/hcps/{hcp_id}`

### Interactions

- POST `/interactions`
- GET `/interactions`
- GET `/interactions/{interaction_id}`
- PUT `/interactions/{interaction_id}`
- DELETE `/interactions/{interaction_id}`

### AI

```http
POST /chat
```

---

## LangGraph

Implemented AI tools:

- ✅ Log Interaction
- ✅ Edit Interaction
- ✅ Search Healthcare Professional
- ✅ Retrieve Interaction History
- ✅ Suggest Follow-up

Workflow:

```text
User
   │
   ▼
POST /chat
   │
   ▼
FastAPI
   │
   ▼
LangGraph
   │
   ▼
Router
   │
   ▼
Selected Tool
   │
   ▼
Service Layer
   │
   ▼
Repository
   │
   ▼
PostgreSQL
   │
   ▼
Structured Response
```

---

## End-to-End AI Workflow Validation

The complete AI workflow has been validated from user request to database persistence.

Validation includes:

- ✅ Intent routing
- ✅ LangGraph execution
- ✅ Tool execution
- ✅ Service layer
- ✅ Repository layer
- ✅ PostgreSQL persistence
- ✅ Structured API responses

Validated workflows:

- Log Interaction
- Edit Interaction
- Search Healthcare Professional
- Retrieve Interaction History
- Suggest Follow-up
---

## License

Created as part of a technical assessment.