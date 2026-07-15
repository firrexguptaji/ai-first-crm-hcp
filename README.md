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
- llama-3.3-70b-versatile

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

MODEL_NAME=llama-3.3-70b-versatile
```

## Frontend

```env
VITE_API_URL=http://localhost:8000
```

> **Note**
>
> The original assignment specified `gemma2-9b-it`. Since the model has been deprecated by Groq, this project uses `llama-3.3-70b-versatile` while preserving the intended LangGraph architecture.

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
| ADR | Architecture decisions |
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
```

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

Workflow

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

# Current Progress

## Milestone 1 — Project Setup

- ✅ Repository Setup
- ✅ Development Environment
- ✅ Documentation Foundation

---

## Milestone 2 — Backend Development

Completed

- ✅ FastAPI
- ✅ PostgreSQL
- ✅ SQLAlchemy ORM
- ✅ Pydantic Schemas
- ✅ Repository Layer
- ✅ Service Layer
- ✅ REST API
- ✅ LangGraph Integration
- ✅ AI Chat Endpoint

Status

**Completed**

---

## Milestone 3 — Frontend Development

Completed

- ✅ Responsive Application Layout
- ✅ Split Screen Layout
- ✅ Redux Toolkit Configuration
- ✅ Read-only Interaction Form
- ✅ AI Assistant Chat Interface
- ✅ Reusable UI Components
- ✅ Axios API Client
- ✅ API Service Layer
- ✅ Frontend ↔ Backend Communication

Next

- Redux Async Integration
- AI Response Rendering
- Automatic Form Population
- Loading & Error States

Status

**In Progress**

---

## Milestone 4 — AI Integration

Completed

- ✅ LangGraph Router
- ✅ Tool Registry
- ✅ AI Workflow
- ✅ Five AI Tools

Status

**Completed**

---

## Milestone 5 — DevOps & Deployment

Planned

- Docker
- Docker Compose
- Production Configuration
- Deployment Guide

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
- ✅ Interaction Form
- ✅ AI Assistant Chat
- ✅ Reusable Components
- ✅ Axios API Client
- ✅ API Service Layer
- ✅ Backend API Communication

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