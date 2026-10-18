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
Router (LLM + keyword fallback)
 │
 ├────────────┬────────────┬────────────┬────────────┬──────────────┐
 ▼            ▼            ▼            ▼            ▼              ▼
Log Tool   Edit Tool   Search Tool   History Tool   Follow-up Tool  Unsupported
 │            │            │            │            │             (no database)
 └────────────┴────────────┴────────────┴────────────┘
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
- Selecting the LangGraph tool (LLM routing, ADR-004)
- Extracting structured data (JSON Schema output, ADR-003)
- Updating CRM interaction data
- Declining unsupported requests without database writes

---

## Database

Stores:

- Healthcare Professionals
- Interaction records
- Future application data

# Frontend Architecture

The frontend follows a component-based architecture using reusable layout components.

## Layout Structure

```text
App
 │
 ▼
HomePage
 │
 ▼
AppLayout
 │
 ├── Header
 │
 └── SplitLayout
        │
        ├── LeftPanel
        └── RightPanel
```

# End-to-End AI Workflow

The AI workflow has been validated from the initial user request through LangGraph execution, business logic, database persistence, and structured API responses.

## Workflow

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
                  │
                  ▼
        Structured JSON Response
```

## Frontend State Management

The frontend uses Redux Toolkit for global state management.

```text
React Components
        │
        ▼
Redux Toolkit Store
        │
 ┌──────┼────────┐
 ▼      ▼        ▼
App   Chat   Interaction
 Slice Slice     Slice
```

The Redux store provides centralized application state while keeping business logic separate from presentation components.