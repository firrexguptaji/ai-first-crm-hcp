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
   Intent Router (keyword-based)
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

## Tools

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

---

## Intent Routing

The router is a deterministic, rule-based classifier (`app/graph/router.py`).

Rules

- Keywords match **whole words only** ("call" does not match "recall", "met" does not match "metformin")
- Rules are checked from **most specific to least specific**
- An edit requires an edit verb **and** a reference to an existing record or field

Priority Order

```text
Edit Interaction        update / change / correct  +  meeting / last / summary / date ...
        │
        ▼
Interaction History     history, past meetings, show interactions ...
        │
        ▼
Suggest Follow-up       suggest, recommend, next step, what should I ...
        │
        ▼
Log Interaction         met, visited, called, discussed ...
        │
        ▼
Search HCP              find, search, list, doctors ...
        │
        ▼
Default                 Log Interaction
```

Examples

| Message | Tool |
|---------|------|
| Update my meeting with Dr. Smith, sentiment was positive | Edit Interaction |
| Suggest a follow-up after my call with Dr. Smith | Suggest Follow-up |
| Met Alice Brown today. Schedule a follow-up next week. | Log Interaction |
| Dr. Smith asked about metformin dosing | Log Interaction |
| Add Dr. Patel as an attendee to my meeting with Alice Brown | Edit Interaction |

Known Limitations

Keyword routing cannot understand meaning. Messages such as *"Alice Brown's sentiment should be neutral"* or *"When did I last meet Alice Brown?"* are misrouted, and unrecognised messages default to Log Interaction. LLM-based intent routing is planned as the next issue.

Routing logic lives in `classify(message)`, which is unit-tested independently of the graph.

---

## LLM Integration

| Item | Value |
|------|-------|
| Provider | Groq |
| Model | `openai/gpt-oss-120b` |
| Temperature | 0 |
| Structured Output | JSON Schema response format |

All tools obtain a schema-bound LLM through a shared helper:

```python
from app.llm.groq import structured

structured_llm = structured(InteractionExtraction)
```

The helper uses Groq's JSON Schema response format instead of forced tool calling, which prevents reasoning models from answering in prose.

See **ADR-003** for the model migration decision.

---

## Date Resolution

Dates are resolved in two steps (`app/graph/tools/dates.py`):

1. The prompt gives the LLM today's date and asks for ISO dates (`YYYY-MM-DD`)
2. A fallback parser resolves common phrases

Supported Phrases

- today, yesterday, tomorrow
- next week, last week
- in N days / weeks
- N days / weeks ago
- ISO dates and datetimes

---

## Error Handling

Tool errors never reach the client as HTTP 500 responses.

```text
Tool Execution
      │
      ├── Success ──────────► Tool Output
      │
      ├── ValueError ───────► Message shown to user
      │                       (e.g. "HCP 'X' not found.")
      │
      └── Unexpected Error ─► Logged on server
                              Generic message shown to user
```

Error Output

```json
{
  "success": false,
  "error_type": "validation",
  "error": "HCP 'Nobody' not found."
}
```

| error_type | Meaning |
|------------|---------|
| `validation` | Expected business error, safe to show |
| `internal` | Unexpected failure, details hidden |

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
- ✅ Whole-word, priority-ordered routing (#69)
- ✅ JSON Schema structured output (#69)
- ✅ Natural-language date resolution (#69)
- ✅ Graceful error handling (#69)
- ✅ Additional interaction fields extracted by AI (#72)

---

# Workflow Validation

The LangGraph workflow has been validated through end-to-end integration testing.

## Registered Tools

- Log Interaction
- Edit Interaction
- Search HCP
- Retrieve Interaction History
- Suggest Follow-up

## Execution Flow

```text
START
   │
   ▼
Router
   │
   ▼
Selected Tool
   │
   ▼
END
```

## Status

All planned LangGraph tools have been implemented.