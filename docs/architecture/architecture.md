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
                 React + Redux
                       │
                       ▼
                FastAPI REST API
                       │
                       ▼
                 LangGraph Graph
                       │
        ┌──────────────┴──────────────┐
        ▼                             ▼
    LangGraph Tools             Groq LLM
        │
        ▼
   Service Layer
        │
        ▼
 Repository Layer
        │
        ▼
 PostgreSQL Database
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
- Business logic
- Database access
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