# Frontend Architecture

## Overview

The frontend is built with React, TypeScript, Redux Toolkit, and Vite following a component-driven architecture. The application provides a responsive split-screen interface where medical representatives interact with an AI assistant while viewing structured Healthcare Professional (HCP) interaction details.

The architecture emphasizes reusable UI components, centralized API communication, centralized state management, and clear separation between presentation, business logic, and backend services.

---

## Technology

- React
- TypeScript
- Redux Toolkit
- Vite
- Axios
- Lucide React

---

## Folder Structure

```text
src/
│
├── api/
│   ├── client.ts
│   ├── chatApi.ts
│   ├── hcpApi.ts
│   └── interactionApi.ts
│
├── app/
├── assets/
├── components/
│   ├── chat/
│   ├── common/
│   ├── form/
│   └── layout/
│
├── features/
│   ├── app/
│   ├── chat/
│   └── interaction/
│       ├── interactionSlice.ts
│       ├── mappers.ts
│       └── formatters.ts
│
├── pages/
├── styles/
└── types/
    ├── chat.ts
    ├── hcp.ts
    ├── interaction.ts
    └── redux.ts
```

---

# Application Layout

The application uses a responsive split-screen interface.

## Layout Components

- AppLayout
- Header
- SplitLayout
- LeftPanel
- RightPanel

## Component Hierarchy

```text
App
│
▼
HomePage
│
▼
AppLayout
│
├── Header
│
└── SplitLayout
    │
    ├── LeftPanel
    │   │
    │   ▼
    │ InteractionForm
    │
    └── RightPanel
        │
        ▼
     ChatPanel
```

---

## Responsive Layout

### Desktop

```text
+-------------------------------+------------------------------+
|                               |                              |
|      Interaction Form         |      AI Assistant Chat       |
|                               |                              |
+-------------------------------+------------------------------+
```

### Mobile

```text
+-------------------------------+
|      Interaction Form         |
+-------------------------------+
|      AI Assistant Chat        |
+-------------------------------+
```

---

# Component Architecture

## Layout Components

- ✅ AppLayout
- ✅ Header
- ✅ SplitLayout
- ✅ LeftPanel
- ✅ RightPanel

---

## Interaction Form Components

- ✅ InteractionForm
- ✅ Input
- ✅ Dropdown
- ✅ TextArea
- ✅ TextAreaWithAction
- ✅ ActionRow
- ✅ InfoCard
- ✅ RadioGroup
- ✅ SuggestionList

---

## AI Assistant Components

- ✅ ChatPanel
- ✅ ChatHeader
- ✅ ChatMessages
- ✅ ChatMessage (status styling, Retry button)
- ✅ ChatInput (Enter to send)
- ✅ ThinkingIndicator

---

## Shared Components

- ✅ Button
- ✅ Input
- ✅ Dropdown
- ✅ TextArea
- ✅ Card
- ✅ Loading
- ✅ EmptyState

---

# API Layer

The frontend communicates with the backend through a centralized Axios client.

## Architecture

```text
React Components
        │
        ▼
API Services
(chatApi, hcpApi, interactionApi)
        │
        ▼
Axios Client
        │
        ▼
FastAPI REST API
```

## Implemented Services

- Chat Service
- Healthcare Professional Service
- Interaction Service

## Responsibilities

- Centralized API configuration
- Environment-based API URL
- Typed request and response models
- Service abstraction
- Basic API error handling

## Client Configuration

| Setting | Value | Reason |
|---------|-------|--------|
| Base URL | `VITE_API_URL` | Environment-based configuration |
| Timeout | 60 seconds | AI requests can make several LLM calls |

## Chat Error Responses

The AI Chat API returns HTTP 200 even when a tool fails. Failures are reported inside `tool_output`:

```json
{
  "response": "HCP 'Nobody' not found.",
  "tool_name": "log_interaction",
  "tool_output": {
    "success": false,
    "error_type": "validation",
    "error": "HCP 'Nobody' not found."
  }
}
```

The chat displays `response` for both success and failure. Line breaks in replies are preserved (`white-space: pre-line`).

| `error_type` | Example |
|--------------|---------|
| `validation` | HCP not found, missing HCP name, nothing to update |
| `unsupported` | Greeting or unsupported request; reply lists capabilities |
| `internal` | Unexpected server error |

## Type Alignment

Frontend types mirror the backend schemas (#60).

| File | Mirrors |
|------|---------|
| `types/hcp.ts` | `schemas/healthcare_professional.py` |
| `types/interaction.ts` | `schemas/interaction.py`, `models/enums.py` |
| `types/chat.ts` | `schemas/chat.py` and each tool's `tool_output` |

`types/chat.ts` provides type guards for reading tool output safely:

- `isInteractionOutput(response)`
- `isHistoryOutput(response)`
- `isFollowUpOutput(response)`
- `isToolError(output)`

---

# Loading & Error Handling

Implemented in #61.

## Request Lifecycle

```text
User presses Enter / Send
        │
        ▼
addUserMessage ──► user bubble
        │
        ▼
sendChatMessage.pending ──► Thinking… indicator, input disabled
        │
        ├── fulfilled ──► assistant bubble (status from tool_output)
        │
        └── rejected ───► error bubble + Retry
```

## Reply Status

Each assistant message has a `status` derived from `tool_output` (`replyStatus()` in `chatSlice.ts`).

| Status | Source | Style |
|--------|--------|-------|
| `ok` | `success: true` | Grey (default) |
| `notice` | `error_type: validation` | Yellow, alert icon |
| `info` | `error_type: unsupported` | Blue, info icon |
| `error` | `error_type: internal`, or request failed | Red, warning icon, **Retry** |

## Request Errors

Failures before a response arrives are converted by `getErrorMessage()` (`api/errors.ts`).

| Failure | Message |
|---------|---------|
| Backend not running / network down | Can't reach the server. Check that the backend is running, then try again. |
| Timeout (60 s) | The AI is taking too long to respond. Please try again. |
| HTTP 5xx | The server ran into a problem. Please try again in a moment. |
| HTTP 422 | The request was not valid. Please rephrase your message. |

## Interaction Context

Every chat request includes `interaction_id`, the interaction currently shown in the form (from the interaction slice). The backend uses it to resolve edits such as "Add Dr. Patel as an attendee". When the form is empty, it is omitted and the assistant asks which interaction to change if the HCP has several.

## Retry

Failed replies store the original message in `retryMessage`. Retry removes the error bubble and sends the message again. Retry is disabled while another request is running.

## Input

| Key | Action |
|-----|--------|
| Enter | Send |
| Shift + Enter | New line |

Enter is ignored while an IME is composing text.

## Other Feedback

- Thinking indicator with animated dots (static when the user prefers reduced motion)
- Auto-scroll to the newest message
- Send button shows "Sending..." and is disabled during a request

---

# State Management

Redux Toolkit is configured as the application's global state management solution.

## Store

Current slices:

- App
- Chat
- Interaction

## Provider

The Redux Provider wraps the root React application and exposes the global store throughout the component tree.

## Typed Hooks

- useAppDispatch
- useAppSelector

These hooks provide fully type-safe access to Redux state and actions.

---

# Automatic Form Population

The Interaction Details form is read-only. It is populated exclusively by AI chat responses.

## Workflow

```text
Chat Input
   │
   ▼
sendChatMessage (Async Thunk)
   │
   ▼
POST /chat
   │
   ▼
sendChatMessage.fulfilled
   │
   ├──────────────► chatSlice
   │                Adds assistant message
   │
   └──────────────► interactionSlice
                    Reads tool_output
                         │
                         ▼
                    mappers.ts
                    snake_case → camelCase
                         │
                         ▼
                    InteractionForm
                    formatters.ts → labels, dates
```

## Update Rules

| Tool | Form Update |
|------|-------------|
| Log Interaction | Shows the saved interaction |
| Edit Interaction | Shows the updated interaction |
| Interaction History | Shows the latest interaction |
| Suggest Follow-up | Adds the recommendation to AI Suggested Follow-ups |
| Search HCP | No change |
| Unsupported | No change |
| Any failed response | No change |

Suggestions are cleared when a different interaction is loaded.

## Field Mapping

| Form Field | State | Backend Field |
|------------|-------|---------------|
| HCP Name | `hcpName` | `tool_output.hcp_name` |
| Interaction Type | `channel` | `channel` |
| Date | `interactionDate` | `interaction_date` |
| Time | `interactionDate` | `interaction_date` |
| Attendees | `attendees` | `attendees` |
| Topics Discussed | `summary` | `summary` |
| Materials Shared | `productsDiscussed` | `products_discussed` |
| Samples Distributed | `samplesDistributed` | `samples_distributed` |
| Observed / Inferred Sentiment | `sentiment` | `sentiment` |
| Outcomes | `outcomes` | `outcomes` |
| Follow-up Actions | `followUpActions`, `followUpDate` | `follow_up_actions`, `follow_up_date` |
| AI Suggested Follow-ups | `suggestions` | `recommendation.recommendation` |

`raw_notes` (the original message) is stored but not displayed.

All form fields are populated by the AI (#72).

## Display Formatting

| Value | Display |
|-------|---------|
| `IN_PERSON` / `PHONE` / `EMAIL` / `VIDEO` / `OTHER` | In Person / Phone / Email / Video / Other |
| `POSITIVE` / `NEUTRAL` / `NEGATIVE` | Positive / Neutral / Negative |
| `2026-10-18T10:30:00` | Date `18-10-2026`, Time `10:30` |
| `follow_up_date: 2026-10-25` | Follow up on 25-10-2026 |
| `follow_up_actions` + `follow_up_date` | Send Phase III data. / Follow up on 25-10-2026 |
| `attendees: ["Nurse Kelly", "Dr. Patel"]` | Nurse Kelly, Dr. Patel |

Dates are read directly from the ISO string, so the browser time zone cannot shift the displayed day.

## Source Badge

| Source | Badge |
|--------|-------|
| `log_interaction` | Logged by AI |
| `edit_interaction` | Updated by AI |
| `interaction_history` | Latest from history |

---

# Frontend Workflow

Current communication flow:

```text
User
   │
   ▼
Chat Input
   │
   ▼
Redux Async Thunk
   │
   ▼
API Layer
   │
   ▼
POST /chat
   │
   ▼
FastAPI
   │
   ▼
LangGraph
   │
   ▼
Selected Tool
   │
   ▼
Structured Response
   │
   ▼
Redux Store
   │
   ├──────────► Chat Messages
   │
   └──────────► Interaction Form
```

---

# Backend API Integration

Implemented REST endpoints:

## AI

- POST `/chat`

## Healthcare Professionals

- GET `/hcps`
- POST `/hcps`
- GET `/hcps/{hcp_id}`
- PUT `/hcps/{hcp_id}`
- DELETE `/hcps/{hcp_id}`

## Interactions

- GET `/interactions`
- POST `/interactions`
- GET `/interactions/{interaction_id}`
- PUT `/interactions/{interaction_id}`
- DELETE `/interactions/{interaction_id}`

---

# UI Design Principles

The frontend follows these engineering principles:

- Component-driven architecture
- Reusable UI components
- Responsive layouts
- Centralized API layer
- Centralized state management
- Consistent styling
- Separation of presentation and business logic
- Type-safe API communication

---

# Development Progress

## Completed

### Layout

- ✅ Responsive Layout
- ✅ Header
- ✅ Split Layout

### State Management

- ✅ Redux Toolkit
- ✅ Store Configuration
- ✅ Typed Hooks

### AI Chat

- ✅ Chat Input
- ✅ Redux Async Thunks
- ✅ Backend Integration
- ✅ Request Lifecycle
- ✅ Conversation History
- ✅ AI Response Rendering
- ✅ Thinking Indicator (#61)
- ✅ Reply Status Styling (#61)
- ✅ Request Error Messages and Retry (#61)
- ✅ Auto-scroll and Enter to Send (#61)

### Components

- ✅ Interaction Form
- ✅ Shared Components
- ✅ Chat Components

### Form Population

- ✅ Additional fields: Attendees, Samples, Outcomes, Follow-up Actions (#72)
- ✅ Backend-aligned Types
- ✅ Interaction Slice populated from AI responses
- ✅ Form bound to Redux
- ✅ Enum labels and date formatting
- ✅ AI Suggested Follow-ups

## Remaining Work

- Interaction history list in chat
- Frontend Unit Tests
- Docker Deployment

---

# Current Status

The frontend foundation, API communication layer, AI chat workflow, automatic form population, and loading and error handling are complete.

The remaining work focuses on deployment and polish.

---

# Docker

Implemented in #63. Files in `frontend/`:

| File | Purpose |
|------|---------|
| `Dockerfile` | Multi-stage build: Node builds, nginx serves |
| `nginx.conf` | Static hosting, SPA fallback, caching, gzip, health check |
| `.dockerignore` | Excludes `node_modules`, `dist` and `.env` |

## Build Stages

```text
Stage 1: node:22-alpine
      │
      ├── npm ci              (cached layer)
      ├── VITE_API_URL        (build argument)
      └── npm run build  ──►  dist/
                               │
Stage 2: nginx:1.27-alpine     │
      │                        ▼
      └── /usr/share/nginx/html  ◄── dist/
```

The final image contains only nginx and the built files; Node.js and the source code are not included.

## Configuration

`VITE_API_URL` is embedded into the JavaScript at **build time**. It is the backend URL as seen from the user's browser.

| Build Argument | Default |
|----------------|---------|
| `VITE_API_URL` | `http://localhost:8000` |

## nginx

| Path | Behaviour |
|------|-----------|
| `/health` | Returns `ok` (container health check) |
| `/assets/*` | Hashed build files, cached for one year |
| `/*` | Falls back to `index.html` (single-page app); not cached |

| Item | Value |
|------|-------|
| Container port | 80 |
| Host port (example) | 8080 |
