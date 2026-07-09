# LangGraph Architecture

## Overview

The project uses a single LangGraph workflow.

A multi-agent architecture is intentionally avoided to keep the solution simple and aligned with the assignment.

---

## Workflow

```text
User Prompt

↓

LangGraph

↓

Router

↓

Tool Selection

↓

Tool Execution

↓

LLM Response

↓

Database Update

↓

API Response
```

---

## Planned Tools

Mandatory

1. Log Interaction
2. Edit Interaction

Additional

3. Search HCP
4. Retrieve Interaction History
5. Suggest Follow-up

---

## Current Status

- LangGraph configured
- Groq configured
- Base graph verified

Tool implementation begins in Milestone 4.