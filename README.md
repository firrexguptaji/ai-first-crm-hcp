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

pip install -r requirements.txt

uvicorn app.main:app --reload
```

---

# Environment Variables

## Backend

```env
GROQ_API_KEY=your_api_key

MODEL_NAME=openai/gpt-oss-120b
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

---

# Documentation

| Document | Description |
|----------|-------------|
| Project Context | Current project status |
| Frontend Architecture | Frontend architecture and workflow |
| Backend Architecture | Backend architecture |
| ADR | Architecture decisions (ADR-001 – ADR-003) |
| Database Schema | ERD and schema documentation |
| Issue Progress | Development roadmap |

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

Reliability

- ✅ Whole-word, priority-ordered intent routing
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

Next

- Loading & Error Handling (#61)

Status

**In Progress**

---

## Milestone 6 — Deployment

Planned

- Backend Dockerfile
- Frontend Dockerfile
- Docker Compose
- Deployment Documentation

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
- ✅ Reusable Components

---

## AI

- ✅ LangGraph Router
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