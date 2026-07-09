# Graph State Design

## Overview

The LangGraph workflow uses a shared state object to carry information between nodes.

Each node reads the current state, performs its task, updates the relevant fields, and returns the updated state.

The state is intentionally lightweight and contains only the information required to process a user request.

---

## State Fields

| Field | Type | Purpose |
|--------|------|---------|
| message | string | Original user message |
| intent | string | Detected user intent |
| tool | string | Selected tool name |
| tool_input | dictionary | Structured input for the selected tool |
| tool_output | dictionary | Result returned by the tool |
| response | string | Final AI response |

---

## State Flow

```text
User Message
      │
      ▼
message
      │
      ▼
Intent Detection
      │
      ▼
intent
      │
      ▼
Tool Selection
      │
      ▼
tool
      │
      ▼
Tool Execution
      │
      ▼
tool_output
      │
      ▼
LLM Response
      │
      ▼
response
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