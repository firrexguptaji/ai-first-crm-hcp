# LangGraph Workflow

## Overview

The LangGraph workflow processes every user request through a single execution path.

Each request follows the same sequence:

1. Receive user input
2. Determine user intent
3. Select the appropriate tool
4. Execute business logic
5. Generate a structured response

This workflow keeps the graph simple while allowing new tools to be added without changing the overall architecture.

---

## Workflow

```text
START
   │
   ▼
Receive User Message
   │
   ▼
Intent Detection
        │
        ▼
Tool Selection
        │
   ┌────┴─────┐
   ▼          ▼
Log       Edit
Interaction Interaction
        │
        ▼
Service Layer
   │
   ▼
Generate Response
   │
   ▼
END
```

---

## Workflow Nodes

### Entry Node

Responsibilities

- Accept user input
- Initialize graph state

Input

- User message

Output

- Initialized graph state

---

### Intent Router

Responsibilities

- Analyze the user request
- Identify the intended operation
- Select the appropriate tool

Possible intents include:

- Log Interaction
- Edit Interaction
- Search HCP
- Retrieve Interaction History
- Suggest Follow-up

---

### Tool Execution

Responsibilities

- Execute the selected tool
- Invoke the Service Layer
- Return structured output

The graph never communicates directly with the database.

---

### Response Generator

Responsibilities

- Receive tool output
- Generate a user-friendly response
- Return the final result

---

## Error Handling

If a tool cannot be selected:

```text
Unknown Request
        │
        ▼
Return clarification request
```

If a tool execution fails:

```text
Tool Error
      │
      ▼
Return structured error response
```

---

## Design Principles

- Single graph
- Sequential execution
- One routing decision per request
- Stateless execution
- Business logic delegated to services