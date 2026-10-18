# LangGraph Workflow

## Overview

The LangGraph workflow processes every user request through a single execution path.

Each request follows the same sequence:

1. Receive user input
2. Determine user intent
3. Select the appropriate tool
4. Execute business logic
5. Generate a structured response

This workflow keeps the graph simple while allowing new tools to be added without changing the overall architecture.

---

## Workflow

```text
START
   │
   ▼
Receive User Message
   │
   ▼
Intent Detection (Router)
   │
   ▼
Tool Selection
   │
   ├─────────────┬─────────────┬─────────────┬────────────────────┐
   ▼             ▼             ▼             ▼                    ▼
Log         Edit          Search HCP   Interaction History   Suggest Follow-up
Interaction Interaction
   │             │             │             │                    │
   └─────────────┴─────────────┴─────────────┴────────────────────┘
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
                    Generate Response
                           │
                           ▼
                          END
```

---

## Workflow Nodes

### Entry Node

Responsibilities

- Accept user input
- Initialize graph state

Input

- User message

Output

- Initialized graph state

---

### Intent Router

Responsibilities

- Analyze the user request
- Identify the intended operation
- Select the appropriate tool

Implementation

- Rule-based classifier in `app/graph/router.py`
- Whole-word keyword matching
- Priority order: Edit → History → Follow-up request → Log → Search
- Unrecognised messages default to Log Interaction

Possible intents include:

- Log Interaction
- Edit Interaction
- Search HCP
- Retrieve Interaction History
- Suggest Follow-up

---

### Tool Execution

Responsibilities

- Execute the selected tool
- Invoke the Service Layer
- Return structured output
- Convert tool errors into structured error responses

The graph never communicates directly with the database.

---

### Response Generator

Responsibilities

- Receive tool output
- Generate a user-friendly response
- Return the final result

---

## Error Handling

Errors are handled at three levels.

### 1. Inside Tools

Incomplete input is rejected before anything is saved.

```text
"Had a chat."
      │
      ▼
HCP name / date / summary missing
(or a placeholder such as "Unknown")
      │
      ▼
success: false
"I couldn't identify a complete interaction..."
```

### 2. Tool Execution Node

```text
Tool Error
      │
      ├── ValueError ──────► success: false, error_type: validation
      │                      Message returned to the user
      │
      └── Other Exception ─► success: false, error_type: internal
                             Logged on server, generic message returned
```

### 3. Chat Endpoint

Any failure outside the tools still returns a valid `ChatResponse` with HTTP 200, so the frontend always receives a message it can display.

---

## Design Principles

- Single graph
- Sequential execution
- One routing decision per request
- Stateless execution
- Business logic delegated to services