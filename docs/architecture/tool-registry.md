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
- Report which required field is missing
- Extract attendees, samples, outcomes and follow-up actions (#72)
- Call the Interaction Service

---

### Edit Interaction

- Update the interaction most recently recorded for an HCP
- Update only the fields the user asked to change
- Ignore empty values returned by the LLM, so unmentioned fields are never wiped
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
| `serialize_interaction()` | `app/graph/tools/serializers.py` | JSON-safe interaction for tool output |

---

## Tool Output Contract

Every tool returns `tool_output` with a `success` flag.

Success

```json
{ "success": true, "...": "tool-specific fields" }
```

Tool-specific Fields

| Tool | Fields |
|------|--------|
| Log Interaction | `interaction_id`, `hcp_name`, `interaction` |
| Edit Interaction | `interaction_id`, `hcp_name`, `interaction` |
| Retrieve Interaction History | `count`, `hcp_name`, `results` (newest first) |
| Search HCP | `count`, `results` |
| Suggest Follow-up | `recommendation.recommendation`, `recommendation.rationale` |

Interaction Shape

Produced by `serialize_interaction()` in `app/graph/tools/serializers.py`.

```json
{
  "id": "uuid",
  "hcp_id": "uuid",
  "interaction_date": "2026-10-18T10:30:00",
  "channel": "IN_PERSON",
  "raw_notes": "Met Alice Brown at her clinic.",
  "summary": "Discussed Product A.",
  "sentiment": "POSITIVE",
  "products_discussed": ["Product A"],
  "follow_up_required": true,
  "follow_up_date": "2026-10-25",
  "attendees": ["Nurse Kelly"],
  "samples_distributed": ["Product A starter pack"],
  "outcomes": "Agreed to trial Product A.",
  "follow_up_actions": "Send Phase III data."
}
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