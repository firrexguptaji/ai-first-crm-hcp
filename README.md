# AI-First CRM HCP Module

> An AI-first Customer Relationship Management (CRM) module for Healthcare Professionals (HCPs) where interaction records are created and managed through an AI assistant powered by LangGraph.

---

# Features

- AI-powered conversational CRM interface
- LangGraph workflow orchestration
- AI-driven interaction logging
- AI-driven interaction editing
- Healthcare Professional search
- Interaction history retrieval
- AI-generated follow-up recommendations
- Loading and error feedback with retry
- FastAPI REST API
- PostgreSQL persistence
- SQLAlchemy ORM
- Redux Toolkit state management
- Responsive split-screen interface
- Reusable frontend component library
- Centralized API service layer
- End-to-end AI workflow

---

# Technology Stack

## Frontend

- React
- TypeScript
- Vite
- Redux Toolkit
- Axios
- Lucide React

## Backend

- FastAPI
- Pydantic v2
- SQLAlchemy 2.0
- PostgreSQL

## AI

- LangGraph
- LangChain
- Groq
- openai/gpt-oss-120b

---

# Project Structure

```text
backend/
database/
docs/
frontend/
README.md
```

---

# Getting Started

## Quick Start (Docker Compose)

Runs PostgreSQL, the backend and the frontend with one command. Requires Docker Desktop.

```powershell
# 1. Configure (only GROQ_API_KEY is required)
Copy-Item .env.example .env
# edit .env and set GROQ_API_KEY

# 2. Start
docker compose up --build
```

| Service | URL |
|---------|-----|
| App | http://localhost:8080 |
| API docs | http://localhost:8000/docs |
| PostgreSQL | localhost:5433 |

Full guide, configuration and troubleshooting: [Deployment Guide](docs/deployment/deployment.md).

A fresh database is seeded with sample Healthcare Professionals (Alice Brown, John Smith, ...). Try:

```text
Met Alice Brown today at her clinic. Discussed Product A, she was positive.
```

| Command | Effect |
|---------|--------|
| `docker compose up -d` | Start in the background |
| `docker compose logs -f backend` | Follow backend logs |
| `docker compose down` | Stop, keep data |
| `docker compose down -v` | Stop and delete the database |

After changing `.env`, run `docker compose up -d` again to recreate the affected containers.

## Local Development

## Frontend

```bash
cd frontend

npm install

npm run dev
```

## Backend

```bash
cd backend

python -m venv .venv

.venv\Scripts\Activate.ps1

# App + test dependencies (requirements.txt holds runtime dependencies only)
pip install -r requirements-dev.txt

uvicorn app.main:app --reload
```

## Backend with Docker

```powershell
# From the project root
docker build -t ai-first-crm-backend ./backend

# Use the local PostgreSQL from inside the container
$url = (Select-String -Path backend\.env -Pattern '^DATABASE_URL=').Line.Split('=', 2)[1].Replace('@localhost', '@host.docker.internal')

docker run --rm --name crm-backend -p 8000:8000 --env-file backend/.env -e "DATABASE_URL=$url" ai-first-crm-backend
```

Check: http://localhost:8000/health

## Frontend with Docker

```powershell
# From the project root
docker build -t ai-first-crm-frontend ./frontend

# Optional: point the UI at another backend URL (baked in at build time)
docker build --build-arg VITE_API_URL=http://localhost:8000 -t ai-first-crm-frontend ./frontend

docker run --rm --name crm-frontend -p 8080:80 ai-first-crm-frontend
```

Open: http://localhost:8080

---

# Environment Variables

## Docker Compose (`.env` in the project root)

See `.env.example`. Required: `GROQ_API_KEY`. Optional: `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `MODEL_NAME`, `ROUTER_MODE`, `SEED_DEMO_DATA`, `VITE_API_URL`.

## Backend (`backend/.env`, local development)

```env
DATABASE_URL=postgresql+psycopg://postgres:password@localhost:5432/ai_first_crm_hcp

GROQ_API_KEY=your_api_key

MODEL_NAME=openai/gpt-oss-120b

# llm (default): LLM routing with keyword fallback | keyword: keyword rules only
ROUTER_MODE=llm
```

## Frontend

```env
VITE_API_URL=http://localhost:8000
```

> **Note**
>
> The original assignment specified `gemma2-9b-it`. Since the model has been deprecated by Groq, this project first moved to `llama-3.3-70b-versatile`, which Groq retired on 2026-08-16, and now uses `openai/gpt-oss-120b` (Groq's recommended replacement) while preserving the intended LangGraph architecture.

---

# Database

Create a PostgreSQL database named:

```text
ai_first_crm_hcp
```

Configure the database connection in:

```text
backend/.env
```

Existing databases created before #72 need migration 001:

```bash
psql -U postgres -d ai_first_crm_hcp -f database/migrations/001_add_interaction_fields.sql
```

---

# Testing

```bash
cd backend

# Unit and integration tests (PostgreSQL and Groq required for integration tests)
pytest -v

# Live LLM routing evaluation (47 Groq calls, about 2 minutes)
# PowerShell
$env:RUN_LLM_EVAL="1"; pytest tests/test_routing_eval.py -v
```

---

# Documentation

| Document | Description |
|----------|-------------|
| [Deployment Guide](docs/deployment/deployment.md) | Docker Compose, configuration, operations, troubleshooting |
| [Project Context](docs/project-context.md) | Current project status |
| [System Architecture](docs/architecture/architecture.md) | High-level architecture |
| [Frontend Architecture](docs/architecture/frontend.md) | Frontend architecture, form population, error handling, Docker |
| [Backend Architecture](docs/architecture/backend.md) | Backend layers, configuration, Docker, Compose |
| [LangGraph](docs/architecture/langgraph.md) | Graph, intent routing, LLM integration |
| [Tool Registry](docs/architecture/tool-registry.md) | AI tools and output contract |
| [Database](docs/architecture/database.md) | Database status, migrations, Compose database |
| [Database Schema](database/schema/schema.md) | Schema and ERD |
| [ADR](docs/adr/README.md) | Architecture decisions (ADR-001 – ADR-004) |
| [Issue Progress](docs/issues/issue-progress.md) | Development roadmap |

---

# System Architecture

```text
                User
                  │
                  ▼
        React Frontend
                  │
                  ▼
          Axios API Client
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

---

# Frontend Architecture

```text
App
│
├── Layout
│   ├── Left Panel
│   │
│   │   └── Interaction Form
│   │       ├── Input
│   │       ├── Dropdown
│   │       ├── TextArea
│   │       ├── Info Card
│   │       ├── Radio Group
│   │       └── Suggestion List
│   │
│   └── Right Panel
│       │
│       └── AI Assistant
│           ├── Header
│           ├── Message List
│           ├── Message Bubble
│           └── Chat Input
│
└── Redux Store
    ├── chat
    └── interaction  ← populated by AI responses
```

## Automatic Form Population

The Interaction Details form is read-only and fills itself from AI chat responses.

| Chat Message | Form |
|--------------|------|
| Met Alice Brown today, discussed Product A, she was positive | Shows the logged interaction |
| Update my meeting with Alice Brown, sentiment was neutral | Shows the updated interaction |
| Show interaction history for Alice Brown | Shows the latest interaction |
| Suggest a follow-up for Alice Brown | Adds an AI suggested follow-up |

---

# API Layer

The frontend communicates with the backend through a centralized Axios client.

```text
React Components
        │
        ▼
API Services
(chatApi, hcpApi, interactionApi)
        │
        ▼
Axios Client
        │
        ▼
FastAPI REST API
```

Implemented:

- Axios API Client
- Environment Configuration
- Chat API Service
- Healthcare Professional API Service
- Interaction API Service
- Typed Request & Response Models
- Basic API Error Handling

---

# REST API

## AI

```http
POST /chat
```

Example request

```json
{
  "message": "Find Alice Brown"
}
```

Example response

```json
{
  "response": "Found 8 Healthcare Professional(s).",
  "tool_name": "search_hcp",
  "tool_output": {
    "success": true,
    "count": 8,
    "results": []
  }
}
```

---

## Healthcare Professionals

- POST `/hcps`
- GET `/hcps`
- GET `/hcps/{hcp_id}`
- PUT `/hcps/{hcp_id}`
- DELETE `/hcps/{hcp_id}`

---

## Interactions

- POST `/interactions`
- GET `/interactions`
- GET `/interactions/{interaction_id}`
- PUT `/interactions/{interaction_id}`
- DELETE `/interactions/{interaction_id}`

---

# LangGraph

Implemented AI tools

- ✅ Log Interaction
- ✅ Edit Interaction
- ✅ Search Healthcare Professional
- ✅ Retrieve Interaction History
- ✅ Suggest Follow-up
- ✅ Unsupported (greetings, capability questions, delete requests — no database writes)

Routing

- ✅ LLM selects the tool, keyword rules as fallback (ADR-004)

| Router | Evaluation (47 messages) |
|--------|--------------------------|
| Keyword | 32 / 47 |
| **LLM** | **47 / 47** |

Reliability

- ✅ Edits change only the fields you mention; add/remove attendees, samples and products
- ✅ JSON Schema structured output
- ✅ Natural-language date resolution ("tomorrow", "next week")
- ✅ Incomplete interactions are never saved
- ✅ Tool errors returned as chat messages, never HTTP 500

Example error response

```json
{
  "response": "HCP 'Nobody' not found.",
  "tool_name": "log_interaction",
  "tool_output": {
    "success": false,
    "error_type": "validation",
    "error": "HCP 'Nobody' not found."
  }
}
```

Workflow

```text
User
   │
   ▼
Chat Interface
   │
   ▼
Redux Toolkit
   │
   ▼
Async Thunk
   │
   ▼
FastAPI
   │
   ▼
LangGraph
   │
   ▼
Selected Tool
   │
   ▼
Service Layer
   │
   ▼
Repository Layer
   │
   ▼
PostgreSQL
   │
   ▼
Structured Response
   │
   ▼
Redux Store
   │
   ▼
Chat Interface
```

---

# Current Progress

## Milestone 1 — Project Setup

- ✅ Repository Setup
- ✅ Development Environment
- ✅ Documentation Foundation

Status

**Completed**

---

## Milestone 2 — Backend Development

- ✅ FastAPI
- ✅ PostgreSQL
- ✅ SQLAlchemy ORM
- ✅ Pydantic Schemas
- ✅ Repository Layer
- ✅ Service Layer
- ✅ REST API

Status

**Completed**

---

## Milestone 3 — Frontend Development

- ✅ Application Layout
- ✅ Responsive Split Layout
- ✅ Redux Toolkit Configuration
- ✅ Interaction Details Form
- ✅ AI Assistant Chat Interface
- ✅ Reusable UI Components
- ✅ Frontend ↔ Backend API Integration

Status

**Completed**

---

## Milestone 4 — LangGraph Integration

- ✅ LangGraph Router
- ✅ Tool Registry
- ✅ Five AI Tools
- ✅ LangGraph ↔ FastAPI Integration
- ✅ End-to-End AI Workflow Validation

Status

**Completed**

---

## Milestone 5 — AI Integration

Completed

- ✅ Redux ↔ Backend Integration
- ✅ AI Chat Workflow
- ✅ AI Workflow Reliability (#69)
- ✅ Automatic Interaction Form Population (#60)
- ✅ Additional Interaction Fields (#72)
- ✅ LLM Intent Routing & Edit Safety (#74)
- ✅ Loading & Error Handling (#61)

Status

**Completed**

---

## Milestone 6 — Deployment

Completed

- ✅ Backend Dockerfile (#62)
- ✅ Frontend Dockerfile (#63)
- ✅ Docker Compose with PostgreSQL and demo data (#64)
- ✅ Deployment Guide (#65)

Status

**Completed**

---

## Milestone 7 — Testing & Demo

Planned

- Frontend Polish
- Demo Video & Project Release

---

# Database

Current entities

- HealthcareProfessional
- Interaction

Implemented

- SQLAlchemy ORM Models
- One-to-Many Relationships
- UUID Primary Keys
- PostgreSQL JSONB
- Repository Layer

Documentation

- `database/schema/schema.md`
- `database/schema/erd.md`
- `database/schema/erd.png`

---

# Verification

## Backend

- ✅ FastAPI
- ✅ PostgreSQL
- ✅ SQLAlchemy ORM
- ✅ Repository Layer
- ✅ Service Layer
- ✅ REST API

---

## Frontend

- ✅ Responsive Layout
- ✅ Redux Store
- ✅ AI Chat Workflow
- ✅ Backend Integration
- ✅ Async Redux Thunks
- ✅ Request Lifecycle
- ✅ Conversation History
- ✅ Interaction Form
- ✅ Automatic Form Population
- ✅ Thinking Indicator, Error Messages and Retry
- ✅ Reusable Components

---

## AI

- ✅ LangGraph Router (LLM + keyword fallback)
- ✅ Routing Evaluation (47 / 47)
- ✅ Tool Registry
- ✅ Log Interaction
- ✅ Edit Interaction
- ✅ Search HCP
- ✅ Retrieve Interaction History
- ✅ Suggest Follow-up

---

# End-to-End Validation

Validated workflow

```text
React
   │
   ▼
Axios
   │
   ▼
FastAPI
   │
   ▼
LangGraph
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

Verified

- ✅ Frontend API Communication
- ✅ LangGraph Routing
- ✅ Tool Execution
- ✅ Repository Layer
- ✅ Database Persistence
- ✅ Structured Responses

---

# License

Created as part of a technical assessment.