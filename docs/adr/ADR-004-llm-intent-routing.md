# ADR-004: LLM Intent Routing with Keyword Fallback

## Status

Accepted

---

## Context

The LangGraph router selected tools with keyword rules.

A routing audit of 37 realistic messages found 14 misroutes. Unrecognised messages defaulted to Log Interaction, which writes to the database:

| Message | Expected | Keyword Router |
|---------|----------|----------------|
| Actually she was negative, not positive | Edit Interaction | Log Interaction |
| When did I last meet Alice Brown? | Interaction History | Log Interaction |
| Do we have an oncologist named Smith? | Search HCP | Log Interaction |
| Mark follow-up as not required for Alice Brown | Edit Interaction | Suggest Follow-up |
| Hi | — | Log Interaction |
| Delete my last interaction with Alice Brown | — | Log Interaction |

Each new phrasing required new keywords, and the assignment describes an **AI-first** CRM.

---

## Decision

1. The **LLM selects the tool** using structured output (`IntentClassification`).
2. A sixth option, **`unsupported`**, handles greetings, capability questions and unsupported actions such as deleting records. It never writes to the database.
3. The **keyword router remains as a fallback** when the LLM call fails.
4. `ROUTER_MODE=keyword` disables LLM routing for offline development and debugging.

```python
def select_tool(message: str) -> str:
    if settings.router_mode == "keyword":
        return classify(message)

    try:
        return llm_classify(message)
    except Exception:
        return classify(message)
```

---

## Architecture

```text
User Message
      │
      ▼
LLM Router ──────────────► log_interaction
(IntentClassification)    edit_interaction
      │                   search_hcp
      │ failure           interaction_history
      ▼                   suggest_followup
Keyword Router            unsupported
```

---

## Evaluation

The evaluation set (`backend/tests/routing_cases.py`) contains 47 messages across all six tools.

| Router | Correct | Accuracy |
|--------|---------|----------|
| Keyword | 32 / 47 | 68% |
| **LLM** | **47 / 47** | **100%** |

Run the live evaluation:

```bash
RUN_LLM_EVAL=1 pytest tests/test_routing_eval.py -v
```

---

## Consequences

### Advantages

- Understands meaning, not keywords
- Unsupported requests no longer create records
- New phrasings need no code changes
- The keyword router keeps the system working if Groq fails

### Trade-offs

- One additional LLM call per message (about 0.5–1 second)
- Routing depends on prompt quality; the evaluation set must be re-run after prompt or model changes
- The fallback router is less accurate than the LLM router

---

## Alternatives Considered

### Extend Keyword Rules

Rejected because:

- Every new phrasing needs new rules
- Rules conflict ("add" in a meeting note vs. an edit)

### Full Tool-calling Agent

Rejected because:

- Larger rewrite of the graph
- Harder to test deterministically
- Single routing decision per message is sufficient for the assignment scope

---

## References

- Issue #74 LLM-based Intent Routing and Edit Safety
- `backend/app/graph/router.py`
- `backend/tests/routing_cases.py`
