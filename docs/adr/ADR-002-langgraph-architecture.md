# ADR-002: LangGraph Architecture

## Status

Accepted

---

## Context

The AI-First CRM requires a workflow capable of understanding user requests, selecting the correct business operation, executing the required logic, and returning structured responses.

The assignment requires a LangGraph-based solution while maintaining a simple and maintainable architecture.

---

## Decision

The project adopts a **single LangGraph architecture**.

The graph is responsible for:

- Receiving user requests
- Determining user intent
- Selecting the appropriate tool
- Executing business operations through the Service Layer
- Returning structured responses

Business logic is delegated to the Service Layer.

Database access is delegated to the Repository Layer.

---

## Architecture

```text
User
 │
 ▼
LangGraph
 │
 ▼
Intent Router
 │
 ▼
Tool
 │
 ▼
Service Layer
 │
 ▼
Repository Layer
 │
 ▼
PostgreSQL
```

---

## Consequences

### Advantages

- Simple architecture
- Easy to maintain
- Easy to extend
- Clear separation of concerns
- One graph for all CRM operations

### Trade-offs

- Single graph may grow as more tools are added.
- Routing node becomes the central decision point.
- Future optimization may require graph decomposition.

These trade-offs are acceptable given the scope of the technical assignment.

---

## Alternatives Considered

### Multi-Agent Architecture

Rejected because:

- Adds unnecessary complexity.
- Harder to debug.
- Outside assignment scope.

### Multiple Independent Graphs

Rejected because:

- Duplicate routing logic.
- Increased maintenance.
- Harder to share state.

---

## Rationale

The single-graph architecture satisfies all assignment requirements while remaining scalable enough for future enhancements.