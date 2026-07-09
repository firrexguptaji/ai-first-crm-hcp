# ADR-001: Project Structure

## Status

Accepted

---

## Context

The project requires a maintainable repository structure that clearly separates frontend, backend, database, and documentation.

The architecture should support issue-driven development and remain easy to explain during technical interviews.

---

## Decision

The repository will follow the following top-level structure:

```text
backend/
frontend/
database/
docs/
README.md
```

The backend follows a layered architecture.

The frontend follows a feature-based structure.

Documentation is maintained separately under the `docs/` directory.

---

## Consequences

### Positive

- Clear separation of responsibilities
- Easy navigation
- Scalable project layout
- Supports documentation-first development

### Negative

- Slightly more folders than a minimal assignment
- Requires discipline to keep documentation updated