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
- ✅ ChatMessage
- ✅ ChatInput

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

The chat displays `response` for both success and failure. Error styling and retry are planned in #61.

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

- Loading & Error UX Improvements (#61)
- Frontend Unit Tests
- Docker Deployment

---

# Current Status

The frontend foundation, API communication layer, AI chat workflow and automatic form population are complete.

The Interaction Details form updates automatically from AI responses. The remaining work focuses on loading and error UX, additional interaction fields and deployment.