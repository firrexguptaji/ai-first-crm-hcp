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
  Intent Router (LLM + fallback)
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

### Fallback

6. Unsupported — replies with capabilities, no database access

---

## Design Principles

- Single graph architecture
- LLM intent routing with deterministic fallback
- Tool-driven execution
- Reusable Service Layer
- Repository pattern for database access
- Separation of concerns
- Stateless graph execution

---

---

## Intent Routing

The router (`app/graph/router.py`) selects one tool per message. See **ADR-004**.

```text
User Message
      │
      ▼
LLM Router (IntentClassification)
      │
      ├── success ─────► selected tool
      │
      └── failure ─────► Keyword Router ─────► selected tool
```

Tools

| Tool | Example |
|------|---------|
| Log Interaction | Met Dr. Smith today, discussed Product A |
| Edit Interaction | Actually she was negative, not positive |
| Interaction History | When did I last meet Alice Brown? |
| Search HCP | Do we have an oncologist named Smith? |
| Suggest Follow-up | What should I do next with Alice Brown? |
| Unsupported | Hi / What can you do? / Delete my last interaction |

Unsupported requests reply with the assistant's capabilities and never write to the database.

Configuration

| `ROUTER_MODE` | Behaviour |
|---------------|-----------|
| `llm` (default) | LLM selects the tool, keywords on failure |
| `keyword` | Keyword rules only |

Keyword Fallback Rules

- Whole-word matching ("call" does not match "recall")
- Priority order: Edit → History → Follow-up request → Log → Search
- An edit requires an edit verb (`update`, `change`, `add`, `remove`, ...) **and** a record or field reference

Evaluation

| Router | Correct (47 messages) |
|--------|-----------------------|
| Keyword | 32 / 47 |
| **LLM** | **47 / 47** |

The evaluation set lives in `backend/tests/routing_cases.py`.

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
- ✅ LLM intent routing with keyword fallback (#74)
- ✅ Unsupported tool (#74)
- ✅ Edit safety: mentioned fields only, add/remove lists (#74)

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