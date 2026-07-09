# System Architecture

## Overview

The AI-First CRM HCP Module follows a simple layered architecture designed for maintainability and easy explanation.

The application is divided into four major layers:

1. Frontend
2. Backend API
3. AI Layer
4. Database

---

## High-Level Architecture

```text
User
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
 ├────────────┬──────────────┬───────────────┐
 ▼            ▼              ▼               ▼
Log Tool   Edit Tool   Search Tool   History Tool
 │            │              │               │
 └────────────┴──────────────┴───────────────┘
                    │
                    ▼
              Service Layer
                    ▼
            Repository Layer
                    ▼
               PostgreSQL
```

---

## Frontend

Responsible for:

- Rendering the user interface
- Displaying interaction details
- Displaying AI chat
- Managing UI state using Redux Toolkit

---

## Backend

Responsible for:

- Exposing REST APIs
- Request validation
- Business logic
- Repository coordination
- ORM model management
- Database persistence
- Executing LangGraph workflows
---

## AI Layer

Responsible for:

- Understanding user prompts
- Selecting appropriate LangGraph tools
- Producing structured outputs
- Updating CRM interaction data

---

## Database

Stores:

- Healthcare Professionals
- Interaction records
- Future application data