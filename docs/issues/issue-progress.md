# Issue Progress

## Milestone 1 — Project Setup — ✅ Completed

| Issue | Status |
|-------|--------|
| #1 Initialize Repository Structure | ✅ Completed |
| #2 Configure GitHub Project Management | ✅ Completed |
| #3 Initialize Frontend | ✅ Completed |
| #4 Initialize Backend | ✅ Completed |
| #5 Configure PostgreSQL & SQLAlchemy | ✅ Completed |
| #6 Configure LangGraph & Groq | ✅ Completed |
| #7 Project Documentation Foundation | ✅ Completed |
| #8 Verify Development Environment | ✅ Completed |

---

## Milestone 2 — Backend Development — ✅ Completed

| Issue | Status |
|-------|--------|
| #9 Design Database Schema | ✅ Completed |
| #10 Implement SQLAlchemy Models | ✅ Completed |
| #11 Create Pydantic Schemas | ✅ Completed |
| #12 Implement Repository Layer | ✅ Completed |
| #13 Implement Service Layer | ✅ Completed |
| #14 Develop HCP API Endpoints | ✅ Completed |
| #15 Develop Interaction API Endpoints | ✅ Completed |

---

## Milestone 3 — Frontend Development — ✅ Completed

| Issue | Status |
|-------|--------|
| #16 Design Application Layout | ✅ Completed |
| #17 Configure Redux Toolkit | ✅ Completed |
| #18 Build Interaction Form | ✅ Completed |
| #19 Build AI Chat Interface | ✅ Completed |
| #20 Create Reusable UI Components | ✅ Completed |
| #21 Integrate Frontend with Backend APIs | ✅ Completed |

---

## Milestone 4 — LangGraph Integration — ✅ Completed

| Issue | Status |
|-------|--------|
| #23 Design LangGraph Architecture | ✅ Completed |
| #24 Log Interaction Tool | ✅ Completed |
| #25 Edit Interaction Tool | ✅ Completed |
| #26 Search HCP Tool | ✅ Completed |
| #27 Retrieve Interaction History Tool | ✅ Completed |
| #28 Suggest Follow-up Tool | ✅ Completed |
| #29 Integrate LangGraph with FastAPI | ✅ Completed |
| #30 End-to-End AI Workflow Validation | ✅ Completed |

---

## Milestone 5 — AI Integration — ✅ Completed

| Issue | Status |
|-------|--------|
| #58 Integrate Redux with Backend Services | ✅ Completed |
| #59 Integrate AI Chat Workflow | ✅ Completed |
| #69 Fix AI Workflow Reliability | ✅ Completed |
| #60 Automatic Interaction Form Population | ✅ Completed |
| #72 Add Additional Interaction Fields | ✅ Completed |
| #74 LLM-based Intent Routing and Edit Safety | ✅ Completed |
| #61 Loading & Error Handling | ✅ Completed |

---

## Milestone 6 — Deployment — 🚧 In Progress

| Issue | Status |
|-------|--------|
| #62 Containerize Backend | 👀 Review |
| #63 Containerize Frontend | ⏳ Ready |
| #64 Configure Docker Compose Environment | ⏳ Ready |
| #65 Deployment Documentation | ⏳ Ready |

---

## Milestone 7 — Testing & Demo — ⏳ Not Started

| Issue | Status |
|-------|--------|
| #22 Polish Frontend Experience | ⏳ Backlog |
| #66 Demo Video & Project Release | ⏳ Backlog |

---

## Issue Notes

### #69 Fix AI Workflow Reliability

| Change | Result |
|--------|--------|
| Whole-word, priority-ordered routing | Edit, history and follow-up requests no longer routed to Log Interaction |
| Model migration to `openai/gpt-oss-120b` | Replaces retired `llama-3.3-70b-versatile` (ADR-003) |
| JSON Schema structured output | Fixes `tool_use_failed` errors |
| Incomplete interaction guard | Incomplete or placeholder data is no longer saved |
| Graceful error handling | Tool errors return chat messages instead of HTTP 500 |
| Natural-language dates in edits | "tomorrow", "next week" supported |
| CORS for local dev origins | Frontend works on any local port |
| Frontend timeout 60s | AI requests no longer time out in the UI |

Tests: 43 → 88 passing.

Live validation: 8 / 8 chat scenarios passing.

### #60 Automatic Interaction Form Population

| Iteration | Change |
|-----------|--------|
| 60a | Log, Edit and History tools return the full interaction (`serialize_interaction`) |
| 60b | Frontend types aligned with backend schemas, typed `tool_output` |
| 60c | `interactionSlice` populated from AI responses |
| 60d | Interaction form bound to Redux, enum labels and date formatting |

Form fields without database columns (Attendees, Samples Distributed) remain empty.

### #72 Add Additional Interaction Fields

| Iteration | Change |
|-----------|--------|
| 72a | Columns `attendees`, `samples_distributed`, `outcomes`, `follow_up_actions`; SQL migration 001 |
| 72b | AI extraction of the new fields |
| 72c | Form shows all fields; Topics Discussed now shows the AI summary |

Fixes found during live testing

| Problem | Fix |
|---------|-----|
| "Add Dr. Patel as an attendee…" routed to Log Interaction | `add`, `remove`, `set`, `replace`, `include` and field names added to edit routing |
| Edit wiped fields the user did not mention | Empty LLM values are ignored |
| Edit changed an older interaction | Edit targets the most recently recorded interaction |
| "today" saved as midnight | Today's date keeps the current time |
| Attendee titles removed ("Patel") | Titles removed from the HCP name only |
| Incomplete-interaction message was vague | Message names the missing field |
| Duplicate HCP names resolved randomly | Oldest matching HCP is always used |

### #74 LLM-based Intent Routing and Edit Safety

| Iteration | Change |
|-----------|--------|
| 74a | LLM intent routing with keyword fallback, Unsupported tool, `ROUTER_MODE` |
| 74b | Routing evaluation set: LLM 47 / 47, keyword 32 / 47 (ADR-004) |
| 74c | Edit applies only mentioned fields; add/remove for lists; "nothing to update" |
| 74d | Placeholder values ("N/A") stored as null |

Fixes found during live testing

| Problem | Fix |
|---------|-----|
| "Actually she was negative" → "HCP 'UNKNOWN' not found" | Ask "Which Healthcare Professional?" |
| LLM returned `hcp_name: null` → parsing error | `hcp_name` optional in AI schemas |
| HCP name missed in "Delete Product B ... with Alice Brown" | Fallback: name taken from the message |
| History did not answer "When did I last meet...?" | Reply includes the latest interaction |
| Capability list shown on one line | Chat bubbles keep line breaks |

Tests: 176 unit and integration tests, plus 47 opt-in live routing evaluations.

### #61 Loading & Error Handling

| Iteration | Change |
|-----------|--------|
| 61a | Request errors classified (network, timeout, server); reply status per message; failed messages stored for retry; `any` removed |
| 61b | Thinking indicator, status colours, Retry button, auto-scroll, Enter to send |

| Status | Shown For |
|--------|-----------|
| Notice (yellow) | Missing HCP name, HCP not found, nothing to update |
| Info (blue) | Greetings and unsupported requests |
| Error (red) + Retry | Server unreachable, timeout, server error |

### #62 Containerize Backend

| Change | Detail |
|--------|--------|
| `backend/Dockerfile` | `python:3.12-slim`, cached dependency layer, non-root user, health check |
| `backend/.dockerignore` | Keeps `.env` and local files out of the image |
| `requirements.txt` | Converted from UTF-16 to UTF-8; runtime dependencies only |
| `requirements-dev.txt` | Test dependencies for local development |

Verified: image builds, container starts, `/health` and `/chat` work against the host PostgreSQL.

### Follow-up Issues

- Conversation context: understand "she" / "that meeting" without repeating the HCP name
- Interaction history list in the chat UI
- Use a separate test database (integration tests currently write to the development database)
- Frontend unit tests (Vitest)
