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

Redux Toolkit will manage:

- Chat state
- Interaction state
- Healthcare Professional state

---

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