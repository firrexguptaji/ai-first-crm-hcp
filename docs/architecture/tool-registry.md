# Tool Registry

## Overview

The LangGraph workflow delegates business operations to a collection of registered tools.

Each tool represents a single responsibility and executes a specific business operation through the Service Layer.

The graph itself contains no business logic.

---

## Tool Registration Strategy

The workflow maintains a centralized tool registry.

The Intent Router selects a tool based on the detected user intent, using the LLM with a keyword fallback (ADR-004).

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
| Unsupported | Reply with capabilities for unsupported requests - IMPLEMENTED |

---

## Tool Responsibilities

### Log Interaction

- Create interaction records
- Validate input
- Reject incomplete input (missing or placeholder HCP name, date or summary)
- Report which required field is missing
- Extract attendees, samples, outcomes and follow-up actions (#72)
- Store placeholder values ("N/A") in optional fields as null (#74)
- Call the Interaction Service

---

### Edit Interaction

- Resolve the target interaction explicitly (`tools/targeting.py`, #81):
  1. Interaction ID in the message (must belong to the HCP)
  2. Date of the existing interaction ("my meeting on 15 October")
  3. Explicit "my last / latest meeting"
  4. Interaction shown in the form (sent by the frontend)
  5. The HCP has only one interaction
  - Otherwise ask which interaction, listing recent ones — **no write**
- Update only the fields the user asked to change
- Ignore empty and placeholder values returned by the LLM
- Apply sentiment, channel and the follow-up flag only when the message mentions them
- Add or remove single attendees, samples and products (`attendees_to_add`, `attendees_to_remove`, ...)
- Reply "I couldn't tell what to change" when nothing would change
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

### Unsupported

- Reply to greetings and capability questions with examples
- Explain that deleting records is not supported
- Never access the database

---

## Shared Helpers

| Helper | Location | Purpose |
|--------|----------|---------|
| `structured(schema)` | `app/llm/groq.py` | Schema-bound LLM using JSON Schema output |
| `parse_date` / `parse_datetime` | `app/graph/tools/dates.py` | Resolve ISO dates and relative phrases |
| `date_rules()` | `app/graph/tools/dates.py` | Prompt rules containing today's date |
| `serialize_interaction()` | `app/graph/tools/serializers.py` | JSON-safe interaction for tool output |
| `resolve_hcp_name()` | `app/graph/tools/validation.py` | HCP name from the LLM, or from the message as fallback |
| `require_hcp_name()` | `app/graph/tools/validation.py` | Ask "Which Healthcare Professional?" when no name is given |
| `clean_text()` / `clean_list()` | `app/graph/tools/validation.py` | Turn empty and placeholder values into null |
| `mentions()` | `app/graph/tools/validation.py` | Whole-word check used by edit safety |
| `resolve_target_interaction()` | `app/graph/tools/targeting.py` | Explicit target resolution for edits |

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

| `error_type` | Meaning |
|--------------|---------|
| `validation` | Expected problem: missing HCP, HCP not found, nothing to update |
| `unsupported` | Request outside the assistant's capabilities |
| `internal` | Unexpected failure, details hidden |

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