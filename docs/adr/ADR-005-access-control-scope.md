# ADR-005: No Authentication in the Assessment Build

## Status

Accepted (demo scope). To be superseded before any production use.

---

## Context

A review (#81) of all API endpoints found no authentication and no per-user authorization. Every caller can read, create, update and delete every HCP and interaction, including through the AI chat endpoint.

The project is a technical assessment. Its scope is the AI-first interaction workflow: LangGraph routing, tool execution, structured extraction and automatic form population. User management is not part of the assignment.

---

## Decision

1. **Do not implement authentication in the assessment build.**
2. **Document the limitation explicitly** instead of implying production readiness:
   - `docs/security/security.md`: endpoint review, findings, required controls
   - README: Security & Limitations section
   - Deployment Guide: warnings before server deployment
3. **Guard the API surface with a test** (`tests/test_api_surface.py`) so new endpoints force a security review update.
4. Keep the existing safeguards that prevent accidental damage (unsupported requests never write, edits need an unambiguous target).

---

## Consequences

### Advantages

- Scope stays on the assignment's AI workflow
- Reviewers see an honest, explicit security posture
- The production path is documented

### Trade-offs

- The application must not be exposed to untrusted networks
- Adding authentication later requires schema changes (record ownership) and query filtering throughout the service layer

---

## Alternatives Considered

### Shared API key

Rejected because:

- Adds a secret to the frontend bundle, where it is visible to every user
- Provides no per-user authorization

### Full OIDC authentication with record ownership

Deferred because:

- Substantial feature outside the assignment scope
- Requires an identity provider and user model

---

## Production Path

1. OIDC authentication, token validation middleware
2. `owner_id` on `healthcare_professionals` and `interactions` (migration)
3. Owner filters in repositories; role checks for deletes
4. Audit log, rate limiting, log redaction

See `docs/security/security.md`.
