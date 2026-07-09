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

## Planned Tools

| Tool | Responsibility |
|------|----------------|
| Log Interaction | Create a new interaction - IMPLEMENTED |
| Edit Interaction | Update an existing interaction - IMPLEMENTED |
| Search HCP | Search Healthcare Professionals - IMPLEMENTED |
| Retrieve Interaction History | Retrieve previous interactions - IMPLEMENTED |
| Suggest Follow-up | Generate follow-up recommendations - PLANNED |

---

## Tool Responsibilities

### Log Interaction

- Create interaction records
- Validate input
- Call the Interaction Service

---

### Edit Interaction

- Update existing interaction records
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