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
├── hooks/
├── pages/
├── styles/
├── types/
│   ├── api.ts
│   ├── chat.ts
│   ├── hcp.ts
│   └── interaction.ts
│
└── utils/
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
   ▼
Chat Messages
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

## Remaining Work

- Automatic Interaction Form Population
- Loading & Error UX Improvements
- Docker Deployment

---

# Current Status

The frontend foundation and API communication layer are complete.

The application successfully communicates with the FastAPI backend through a centralized service layer. The remaining work focuses on Redux integration, AI response rendering, automatic interaction form updates, and completing the end-to-end AI workflow.