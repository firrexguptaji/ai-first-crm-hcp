# Graph State Design

## Overview

The LangGraph workflow uses a shared state object to carry information between nodes.

Each node reads the current state, performs its task, updates the relevant fields, and returns the updated state.

The state is intentionally lightweight and contains only the information required to process a user request.

---

## State Fields

Defined in `app/graph/state.py` (`CRMState`).

| Field | Type | Written By | Purpose |
|-------|------|------------|---------|
| message | string | Chat API | Original user message |
| tool_name | string | Router | Selected tool |
| tool_input | dictionary | Tool | Structured data extracted by the LLM |
| tool_output | dictionary | Tool | Result returned by the tool |
| response | string | Tool | Message shown to the user |
| context | dictionary (optional) | Chat API | Request context, e.g. `interaction_id` of the interaction shown in the form (#81) |

---

## State Flow

```text
POST /chat
      │
      ▼
message
      │
      ▼
Router (LLM + keyword fallback)
      │
      ▼
tool_name
      │
      ▼
Tool Execution
      │
      ├── tool_input   (LLM extraction)
      ├── tool_output  (success or structured error)
      └── response     (chat message)
      │
      ▼
ChatResponse { response, tool_name, tool_output }
```

---

## Design Principles

- Keep the state minimal
- Avoid storing database models
- Avoid storing SQLAlchemy sessions
- Store only data required by the workflow
- Each node updates only the fields it owns

---

## Future Extension

Additional fields may be introduced in future iterations, including:

- conversation_history
- user_context
- execution_metadata
- confidence_score

The initial implementation keeps the state intentionally simple to align with the project scope.