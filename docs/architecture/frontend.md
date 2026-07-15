# Frontend Architecture

## Overview

The frontend is built with React and TypeScript and follows a component-based architecture. The UI is designed as a responsive split-screen interface where the left panel displays interaction details and the right panel provides an AI assistant chat.

---

## Technology

- React
- TypeScript
- Redux Toolkit
- Vite

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
    └── RightPanel
```

---

## Responsive Design

### Desktop

```text
+-----------------------------+----------------------------+
|                             |                            |
|      Left Panel             |      Right Panel           |
|                             |                            |
+-----------------------------+----------------------------+
```

### Mobile

```text
+-----------------------------+
|        Left Panel           |
+-----------------------------+
|        Right Panel          |
+-----------------------------+
```

---

## Current Components

### Layout

- ✅ AppLayout
- ✅ Header
- ✅ SplitLayout
- ✅ LeftPanel
- ✅ RightPanel

---

## Upcoming Components

### Interaction

- Interaction Details Form
- Form Sections
- Material Cards
- Follow-up Section

### AI Assistant

- Chat Panel
- Chat History
- Chat Input
- Message Components

### Shared Components

- Buttons
- Cards
- Inputs
- Loading States
- Empty States

---

## State Management

Redux Toolkit is configured as the global state management solution.

### Store

The application store combines the following feature slices:

- App
- Chat
- Interaction

### Provider

The Redux Provider wraps the root React application, making the global store available throughout the component tree.

### Typed Hooks

Typed hooks are provided for:

- useAppDispatch
- useAppSelector

These hooks simplify dispatching actions and selecting state while maintaining full TypeScript support.

## API Integration

The frontend will communicate with the FastAPI backend through:

- `/chat`
- `/hcps`
- `/interactions`

The AI assistant will be the primary interface for creating and updating interaction records.

---

## Development Progress

### Completed

- ✅ Responsive application layout
- ✅ Header
- ✅ Split-screen layout
- ✅ Reusable layout components

### In Progress

- 🚧 Interaction Details Form

### Planned

- AI Assistant Chat
- Redux Integration
- Backend Integration
- End-to-End Frontend Workflow


## Interaction Form

Implemented components:

- Input
- Dropdown
- TextArea
- TextAreaWithAction
- ActionRow
- InfoCard
- RadioGroup
- SuggestionList

Features:

- Read-only interaction form
- Responsive grid layout
- CRM-style reusable components
- Icon-enhanced inputs
- Redux-ready architecture



## Chat Components

Implemented components

- ChatPanel
- ChatHeader
- ChatMessages
- ChatMessage
- ChatInput

Features

- Responsive chat layout
- Reusable message bubbles
- User/Assistant message support
- Send button UI
- Static conversation history
- Ready for Redux integration