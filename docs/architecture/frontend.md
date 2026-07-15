# Frontend Architecture

## Overview

The frontend is built with React, TypeScript, and Redux Toolkit following a component-based architecture. The application provides a responsive split-screen interface where users interact with an AI assistant while viewing structured Healthcare Professional (HCP) interaction details.

The architecture emphasizes reusable UI components, centralized state management, and separation of concerns to simplify future AI integration.

---

## Technology

- React
- TypeScript
- Redux Toolkit
- Vite
- Lucide React

---

## Folder Structure

```text
src/
│
├── api/
├── app/
├── assets/
├── components/
│   ├── chat/
│   ├── common/
│   ├── form/
│   └── layout/
├── features/
├── hooks/
├── pages/
├── styles/
├── types/
└── utils/
```

---

## Layout

The application uses a responsive split-screen layout.

### Layout Components

- AppLayout
- Header
- SplitLayout
- LeftPanel
- RightPanel

### Component Hierarchy

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

## Responsive Design

### Desktop

```text
+-------------------------------+------------------------------+
|                               |                              |
|       Interaction Form        |      AI Assistant Chat       |
|                               |                              |
+-------------------------------+------------------------------+
```

### Mobile

```text
+-------------------------------+
|       Interaction Form        |
+-------------------------------+
|      AI Assistant Chat        |
+-------------------------------+
```

---

# Component Architecture

## Layout

- ✅ AppLayout
- ✅ Header
- ✅ SplitLayout
- ✅ LeftPanel
- ✅ RightPanel

---

## Interaction Form

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

## AI Assistant

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
- ✅ Loading
- ✅ EmptyState

---

## State Management

Redux Toolkit is configured as the global state management solution.

### Store

The application store contains three feature slices:

- App
- Chat
- Interaction

### Provider

The Redux Provider wraps the root application and exposes the global store throughout the component tree.

### Typed Hooks

Custom typed hooks are provided:

- useAppDispatch
- useAppSelector

These provide type-safe access to Redux state and actions.

---

## Frontend Workflow

The intended application workflow is:

```text
User
   │
   ▼
AI Assistant Chat
   │
   ▼
Redux
   │
   ▼
FastAPI API
   │
   ▼
LangGraph
   │
   ▼
Selected AI Tool
   │
   ▼
Structured Response
   │
   ▼
Redux Store Update
   │
   ▼
Interaction Form Updates
```

---

## API Integration

The frontend communicates with the FastAPI backend using REST APIs.

### Endpoints

- POST `/chat`
- GET `/hcps`
- POST `/hcps`
- GET `/interactions`
- POST `/interactions`

The AI Assistant serves as the primary user interface for creating and updating interaction records.

---

## UI Design Principles

The frontend follows several design principles:

- Component-based architecture
- Reusable UI components
- Responsive layouts
- Centralized state management
- Consistent styling
- Clear separation of presentation and business logic

---

## Development Progress

### Completed

#### Layout

- ✅ Responsive Application Layout
- ✅ Header
- ✅ Split Layout

#### State Management

- ✅ Redux Toolkit Configuration
- ✅ Store Configuration
- ✅ Provider Configuration
- ✅ Typed Hooks

#### Interaction Form

- ✅ Interaction Details Form
- ✅ Reusable Form Components
- ✅ Read-only Layout

#### AI Assistant

- ✅ Chat Interface
- ✅ Message History
- ✅ Chat Input
- ✅ Send Action

#### Shared Components

- ✅ Button
- ✅ Loading
- ✅ EmptyState

---

## Remaining Work

- Frontend ↔ Backend Integration
- LangGraph Response Rendering
- Automatic Form Population
- Loading & Error States
- End-to-End Workflow Validation
- Docker Deployment

---

## Current Status

Frontend foundation is complete.

The remaining implementation focuses on integrating the frontend with the existing FastAPI and LangGraph backend to enable end-to-end AI-driven interaction management.