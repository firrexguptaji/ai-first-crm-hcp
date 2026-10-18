# ADR-003: Groq Model Migration and Structured Output

## Status

Accepted

---

## Context

The assignment specified `gemma2-9b-it`. That model was deprecated by Groq, so the project moved to `llama-3.3-70b-versatile`.

Groq retired `llama-3.3-70b-versatile` on **2026-08-16**. Every LLM call then failed with:

```text
404 model_not_found
```

Groq's recommended replacement is `openai/gpt-oss-120b`.

After switching models, the Suggest Follow-up tool failed intermittently:

```text
400 tool_use_failed
Tool choice is required, but model did not call a tool
```

`with_structured_output()` used forced tool calling by default. The new reasoning model sometimes answered in prose instead of calling the tool.

---

## Decision

1. Use **`openai/gpt-oss-120b`** as the default model, configured through `MODEL_NAME`.
2. Obtain structured output through a shared helper that uses Groq's **JSON Schema response format** instead of forced tool calling.

```python
def structured(schema):
    return llm.with_structured_output(
        schema,
        method="json_schema",
    )
```

All LangGraph tools use `structured(...)`.

---

## Architecture

```text
LangGraph Tool
      │
      ▼
structured(Schema)
      │
      ▼
ChatGroq (openai/gpt-oss-120b)
      │
      ▼
JSON Schema Response
      │
      ▼
Pydantic Model
```

---

## Consequences

### Advantages

- All AI tools work again
- Output is constrained to the schema, so prose answers are no longer possible
- One place to change structured-output behaviour
- The model can be changed through configuration only

### Trade-offs

- Reasoning model responses are slower than the previous model
- The frontend API timeout was raised from 10s to 60s
- The project depends on Groq's model availability

---

## Alternatives Considered

### `qwen/qwen3.6-27b`

Rejected because:

- Scheduled for deprecation on 2026-09-14

### Keep forced tool calling and retry on failure

Rejected because:

- Adds latency and cost
- Does not remove the root cause

---

## Rationale

`openai/gpt-oss-120b` is Groq's recommended replacement, and JSON Schema output removes the failure mode without changing tool logic or prompts.

---

## References

- [Groq Model Deprecations](https://console.groq.com/docs/deprecations)
- Issue #69 Fix AI Workflow Reliability
