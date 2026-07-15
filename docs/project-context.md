# AI-First CRM HCP — Project Context

## Project Overview

**Project:** AI-First CRM HCP Module

### Objective

Develop an AI-first CRM module for Healthcare Professionals (HCPs) where interaction records are created, edited, and managed exclusively through a LangGraph-powered AI assistant.

The project follows a production-inspired engineering workflow using issue-driven development, modular architecture, documentation-first practices, and incremental feature delivery.

---

# Technology Stack

## Frontend

- React
- TypeScript
- Vite
- Redux Toolkit
- Lucide React

## Backend

- FastAPI
- SQLAlchemy 2.0
- PostgreSQL
- Pydantic v2

## AI

- LangGraph
- LangChain
- Groq
- llama-3.3-70b-versatile

---

# Engineering Principles

- One Issue = One Feature
- One Feature = One Pull Request
- Documentation updated after every completed issue
- ADRs for significant architectural decisions
- Incremental development
- Component reusability
- Keep architecture within assignment scope

---

# Current Project Status

| Area | Status |
|-------|--------|
| Repository Setup | ✅ |
| Documentation | ✅ |
| Backend Development | ✅ |
| Database | ✅ |
| REST APIs | ✅ |
| LangGraph | ✅ |
| Frontend Foundation | ✅ |
| Frontend Integration | 🚧 |
| Docker Deployment | ⏳ |

---

# Repository Structure

```text
backend/
database/
docs/
frontend/
README.md
```

---

# Architecture Overview

```text
React Frontend
        │
        ▼
Redux Store
        │
        ▼
FastAPI
        │
        ▼
LangGraph Router
        │
        ▼
Selected AI Tool
        │
        ▼
Service Layer
        │
        ▼
Repository Layer
        │
        ▼
SQLAlchemy ORM
        │
        ▼
PostgreSQL
```

---

# Backend Status

## Completed

- FastAPI Application
- SQLAlchemy ORM Models
- Pydantic Schemas
- Repository Layer
- Service Layer
- REST APIs
- PostgreSQL Integration
- LangGraph Router
- Tool Registry
- AI Chat Endpoint
- End-to-End Backend Validation

---

# Frontend Status

## Completed

### Layout

- Responsive Layout
- Header
- Split Layout
- Left Panel
- Right Panel

### State Management

- Redux Toolkit
- Store Configuration
- Provider
- Typed Hooks

### Interaction Form

- Read-only Interaction Form
- Reusable Form Components

### AI Assistant

- Chat Panel
- Chat Header
- Chat Messages
- Chat Input

### Shared Components

- Button
- Input
- Dropdown
- TextArea
- Loading
- EmptyState
- InfoCard
- RadioGroup
- SuggestionList
- ActionRow

---

# AI Status

## Implemented LangGraph Tools

- ✅ Log Interaction
- ✅ Edit Interaction
- ✅ Search Healthcare Professional
- ✅ Retrieve Interaction History
- ✅ Suggest Follow-up

---

# Database Status

## Entities

- HealthcareProfessional
- Interaction

## Relationship

```text
HealthcareProfessional
        │
        │ 1
        ▼
Interaction
        *
```

## Completed

- Schema Design
- SQLAlchemy Models
- Relationships
- Repository Layer

---

# Assignment Constraints

- Read-only interaction form
- AI chat is the primary interaction interface
- LangGraph orchestration
- Five AI tools
- Single-agent workflow
- Production-style engineering practices

---

# Development Workflow

```text
Issue
   │
   ▼
Feature Branch
   │
   ▼
Implementation
   │
   ▼
Testing
   │
   ▼
Documentation
   │
   ▼
Commit
   │
   ▼
Pull Request
   │
   ▼
Merge
```

---

# Current Milestones

## ✅ Milestone 1

Project Setup

## ✅ Milestone 2

Backend Development

## ✅ Milestone 3

Frontend Foundation

## 🚧 Milestone 4

Frontend ↔ Backend Integration

## ⏳ Milestone 5

Docker & Deployment

---

# Remaining Work

## Frontend Integration

- Connect Chat to FastAPI
- Redux Async Actions
- AI Response Rendering
- Automatic Form Population
- Loading & Error Handling

## Deployment

- Backend Dockerfile
- Frontend Dockerfile
- Docker Compose
- Environment Configuration
- One-command Setup

---

# Current Snapshot

| Item | Value |
|------|-------|
| Version | v0.3.0 |
| Milestone | Frontend Integration |
| Completed Issues | #1–#21, #23–#29 |
| Current Issue | #22 Polish Frontend Experience |
| Active Branch | feature/22-Polish-Frontend-Experience |
| Backend | ✅ Complete |
| Frontend Foundation | ✅ Complete |
| AI Integration and Development | ⏳ Pending |