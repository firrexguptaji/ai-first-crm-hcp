# Changelog

## v1.0.1 — 2026-10-20

Documentation update. No code changes.

### Documentation

- Walkthrough now has all 12 screenshots (follow-up, unsupported request, error and retry, mobile layout, API docs, tests added)

### Known Issues

- The follow-up suggestion prompt does not restrict the model to facts from the interaction history, so a suggestion may mention details that were never logged
- `@app.on_event("startup")` is deprecated in FastAPI (3 warnings in pytest)

---

## v1.0.0 — 2026-10-18

First release of the AI-First CRM HCP module.

### Highlights

- **AI-first workflow:** Healthcare Professional interactions are logged and edited through a chat assistant; the Interaction Details form is read-only and fills automatically.
- **LangGraph** with six tools: Log Interaction, Edit Interaction, Search HCP, Interaction History, Suggest Follow-up, Unsupported.
- **LLM intent routing** with keyword fallback: 47 / 47 on the routing evaluation set (keyword only: 32 / 47) — ADR-004.
- **Safe edits:** only mentioned fields change; add/remove list values; ambiguous targets ask instead of guessing; unsupported requests never write.
- **Full form coverage:** attendees, samples, outcomes and follow-up actions extracted by the AI.
- **Docker Compose:** PostgreSQL, backend and frontend with one command, plus demo data.
- **Tests:** about 280 tests, database tests on a separate rolled-back test database, opt-in live Groq tests.
- **Accessible, responsive UI:** labelled controls, live chat log, keyboard focus, tablet and phone layouts.

### Issues

| Area | Issues |
|------|--------|
| Project setup | #1–#8 |
| Backend | #9–#15 |
| Frontend | #16–#21, #22 |
| LangGraph | #23–#30 |
| AI integration | #58–#61, #69, #72, #74 |
| Deployment | #62–#65 |
| Review fixes | #81 |
| Release | #66 |

### Architecture Decisions

- ADR-001 Project Structure
- ADR-002 LangGraph Architecture
- ADR-003 Groq Model Migration and Structured Output (`openai/gpt-oss-120b`)
- ADR-004 LLM Intent Routing with Keyword Fallback
- ADR-005 No Authentication in the Assessment Build

### Known Limitations

- **No authentication or authorization** — demo use only (ADR-005, `docs/security/security.md`)
- No conversation memory: each message must name the HCP
- CORS allows `localhost` origins only
- Database migrations are manual SQL scripts
- Groq free tier has request rate limits; heavy use returns errors until the quota resets (use **Retry**)
- Backend container runs in UTC, so stored interaction times can differ from the local chat time

### Upgrade Notes

Local databases created before #72 need `database/migrations/001_add_interaction_fields.sql`. Docker Compose databases need no migration.
