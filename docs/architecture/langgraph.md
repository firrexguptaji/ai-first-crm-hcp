# LangGraph Architecture

## Overview

The AI-First CRM uses a single LangGraph workflow to process every user request.

The graph is responsible for:

- Receiving natural language requests
- Determining user intent
- Selecting the appropriate AI tool
- Executing business logic through the Service Layer
- Returning structured responses to the user

A multi-agent architecture is intentionally avoided to keep the solution simple, maintainable, and aligned with the assignment requirements.

---

## Architecture

```text
                User
                  │
                  ▼
          LangGraph Graph
                  │
                  ▼
           Intent Router
                  │
      ┌───────────┼────────────┐
      ▼           ▼            ▼
 HCP Tools   Interaction Tools  AI Utilities
      │           │            │
      └───────────┼────────────┘
                  ▼
           Service Layer
                  ▼
        Repository Layer
                  ▼
            PostgreSQL
```

---

## Workflow

```text
User Prompt
      │
      ▼
Graph Entry
      │
      ▼
Intent Detection
      │
      ▼
Tool Selection
      │
      ▼
Tool Execution
      │
      ▼
Service Layer
      │
      ▼
Repository Layer
      │
      ▼
Database
      │
      ▼
LLM Response
      │
      ▼
User
```

---

## Graph Responsibilities

The LangGraph workflow is responsible for:

- Parsing user requests
- Determining user intent
- Selecting the correct tool
- Executing business operations
- Returning structured AI responses

The graph does **not**:

- Access the database directly
- Contain business logic
- Execute SQL queries
- Manage HTTP requests

---

## Planned Tools

### Mandatory

1. Log Interaction
2. Edit Interaction

### Additional

3. Search Healthcare Professional
4. Retrieve Interaction History
5. Suggest Follow-up

---

## Design Principles

- Single graph architecture
- Intent-based routing
- Tool-driven execution
- Reusable Service Layer
- Repository pattern for database access
- Separation of concerns
- Stateless graph execution

---

## Current Status

Implemented

- ✅ Graph State
- ✅ Tool Registry
- ✅ Routing Node
- ✅ Log Interaction Tool
- ✅ Edit Interaction Tool
- ✅ Search HCP Tool
- ✅ Retrieve Interaction History Tool
- ✅ Suggest Follow-up Tool


## Status

All planned LangGraph tools have been implemented.