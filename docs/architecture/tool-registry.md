# Tool Registry

## Overview

The LangGraph workflow delegates business operations to a collection of registered tools.

Each tool represents a single responsibility and executes a specific business operation through the Service Layer.

The graph itself contains no business logic.

---

## Tool Registration Strategy

The workflow maintains a centralized tool registry.

The Intent Router selects a tool based on the detected user intent.

```text
User Request
      │
      ▼
Intent Detection
      │
      ▼
Tool Registry
      │
      ▼
Selected Tool
```

The selected tool executes the required business operation and returns a structured result to the graph.

---

## Registered Tools

| Tool | Responsibility |
|------|----------------|
| Log Interaction | Create a new interaction - IMPLEMENTED |
| Edit Interaction | Update an existing interaction - IMPLEMENTED |
| Search HCP | Search Healthcare Professionals - IMPLEMENTED |
| Retrieve Interaction History | Retrieve previous interactions - IMPLEMENTED |
| Suggest Follow-up | Generate follow-up recommendations - IMPLEMENTED |

---

## Tool Responsibilities

### Log Interaction

- Create interaction records
- Validate input
- Reject incomplete input (missing or placeholder HCP name, date or summary)
- Call the Interaction Service

---

### Edit Interaction

- Update the latest interaction for an HCP
- Update only the fields the user asked to change
- Resolve natural-language dates ("tomorrow", "next week")
- Reject dates that cannot be understood with a clear message
- Call the Interaction Service

---

### Search HCP

- Search Healthcare Professionals
- Return matching records

---

### Retrieve Interaction History

- Retrieve interaction history for an HCP
- Return chronological records

---

### Suggest Follow-up

- Analyze interaction history
- Generate AI-assisted follow-up suggestions

---

## Shared Helpers

| Helper | Location | Purpose |
|--------|----------|---------|
| `structured(schema)` | `app/llm/groq.py` | Schema-bound LLM using JSON Schema output |
| `parse_date` / `parse_datetime` | `app/graph/tools/dates.py` | Resolve ISO dates and relative phrases |
| `date_rules()` | `app/graph/tools/dates.py` | Prompt rules containing today's date |

---

## Tool Output Contract

Every tool returns `tool_output` with a `success` flag.

Success

```json
{ "success": true, "...": "tool-specific fields" }
```

Failure

```json
{ "success": false, "error_type": "validation", "error": "..." }
```

---

## Design Principles

- One tool = One responsibility
- Tools are stateless
- Tools use the Service Layer
- Tools never access the database directly
- Tools return structured outputs

---

## Future Expansion

The registry can be extended with additional tools without changing the graph architecture.

Examples include:

- Delete Interaction
- Create Healthcare Professional
- Update Healthcare Professional
- CRM Analytics
- Reporting