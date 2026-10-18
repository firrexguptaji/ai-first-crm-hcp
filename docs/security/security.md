# Security & Limitations

> **Status: demo / assessment build. Not production-ready.**
>
> The application has **no authentication and no authorization**. Anyone who can reach the API can read, create, change and delete every record. Run it only on a local machine or a trusted private network.

Reviewed in #81 (2026-10-18). Decision recorded in **ADR-005**.

---

# Endpoint Review

| Method | Path | Effect | Authentication | Authorization |
|--------|------|--------|----------------|---------------|
| GET | `/health` | Health check | None (intended) | — |
| POST | `/chat` | AI workflow: reads, **creates and updates** interactions | ❌ None | ❌ None |
| POST | `/hcps` | Create HCP | ❌ None | ❌ None |
| GET | `/hcps` | List all HCPs, including **email and phone** | ❌ None | ❌ None |
| GET | `/hcps/{hcp_id}` | Read HCP | ❌ None | ❌ None |
| PUT | `/hcps/{hcp_id}` | Update HCP | ❌ None | ❌ None |
| DELETE | `/hcps/{hcp_id}` | Delete HCP **and all its interactions** (cascade) | ❌ None | ❌ None |
| POST | `/interactions` | Create interaction | ❌ None | ❌ None |
| GET | `/interactions` | List **all** interactions | ❌ None | ❌ None |
| GET | `/interactions/{interaction_id}` | Read interaction | ❌ None | ❌ None |
| PUT | `/interactions/{interaction_id}` | Update interaction | ❌ None | ❌ None |
| DELETE | `/interactions/{interaction_id}` | Delete interaction | ❌ None | ❌ None |
| GET | `/docs`, `/openapi.json` | Interactive API documentation | None | — |

`tests/test_api_surface.py` fails when an endpoint is added or removed, so this table must be reviewed with every API change.

## Findings

| # | Finding | Severity (if exposed) |
|---|---------|-----------------------|
| 1 | No authentication on any endpoint | Critical |
| 2 | No per-user data: records have no owner, every caller sees all data | Critical |
| 3 | `DELETE /hcps/{id}` deletes an HCP and all interactions, unauthenticated | High |
| 4 | HCP contact details (email, phone) are readable by anyone | High |
| 5 | The chat assistant refuses deletes, but the REST API allows them | Medium |
| 6 | No rate limiting: `/chat` can be used to consume the Groq quota | Medium |
| 7 | Error logs contain the full chat message (may include personal or medical details) | Medium |
| 8 | Docker Compose publishes PostgreSQL on port 5433 | Medium |
| 9 | `/docs` exposes the full API for interactive use | Low |
| 10 | CORS is limited to `localhost`; this restricts browsers only, not other clients (curl, scripts) | Info |

---

# Existing Safeguards

These reduce mistakes; they are **not** access control.

| Safeguard | Where |
|-----------|-------|
| Secrets in `.env`, git-ignored and excluded from Docker images | `.gitignore`, `.dockerignore` |
| Request validation (422 for empty, oversized or malformed requests) | `schemas/chat.py`, Pydantic schemas |
| Unsupported or unrecognised chat requests never write | Router (`unsupported`), ADR-004 |
| Edits require an unambiguous target, otherwise the assistant asks | `tools/targeting.py` |
| Edits change only the fields the user mentions | `tools/edit_interaction.py` |
| Internal errors are logged, not returned to the client | `graph/graph.py`, `api/chat.py` |
| Backend container runs as a non-root user | `backend/Dockerfile` |
| Tests run on a separate database and roll back | `tests/conftest.py` |

---

# AI-specific Risks

| Risk | Current behaviour |
|------|-------------------|
| Prompt injection in chat messages | The LLM can only choose one of six tools and fill typed fields. It cannot run arbitrary actions, but it can be talked into editing any HCP's interaction, because there is no authorization. |
| Wrong tool or wrong record | LLM routing is evaluated (47 / 47); edits ask when the target is ambiguous. |
| Hallucinated values | Placeholders are dropped; unmentioned fields are not changed. Values the user did not say can still be extracted incorrectly. Review records before relying on them. |
| Data sent to a third party | Chat messages and interaction history are sent to the Groq API. Do not enter real patient or confidential data. |

---

# Required Before Production

| Area | Requirement |
|------|-------------|
| Authentication | Identity provider (OIDC/OAuth2, e.g. Auth0, Entra ID, Keycloak); validate tokens on every endpoint except `/health` |
| Data ownership | `owner_id` (or territory/team) on HCPs and interactions; set from the authenticated user |
| Authorization | Every query filtered by owner/team; role checks for delete and HCP management |
| Destructive operations | Restrict or soft-delete; audit who changed what |
| Audit log | Record create/update/delete with user and timestamp |
| Rate limiting | Per-user limits on `/chat` |
| Data protection | Redact message content from logs; data processing agreement with the LLM provider |
| Network | HTTPS only; database not published; `/docs` disabled or protected |
| CORS | Explicit list of production origins |

---

# Running Safely Today

- Run on `localhost` or a private network only
- Use demo data (`SEED_DEMO_DATA=true`), not real HCP or patient data
- Do not publish ports 8000, 8080 or 5433 to the internet
- See the server checklist in [Deployment Guide](../deployment/deployment.md#deploying-to-a-server)
