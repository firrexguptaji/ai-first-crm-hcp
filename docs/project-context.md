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
- openai/gpt-oss-120b

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
| AI Workflow Reliability | ✅ |
| Automatic Form Population | ✅ |
| Additional Interaction Fields | ✅ |
| LLM Intent Routing & Edit Safety | ✅ |
| Loading & Error Handling | ✅ |
| Backend Container | ✅ |
| Frontend Container | ✅ |
| Docker Compose | ✅ |
| Deployment Guide | ✅ |
| Review Fixes (#81) | ✅ |
| Frontend Polish (#22) | ✅ |
| Walkthrough & Release (#66) | 👀 |
| Authentication | ❌ Out of scope (ADR-005) |
| Frontend Integration | 🚧 |
| Docker Deployment | ✅ |

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
- AI Workflow Reliability Fixes (#69)

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
- Automatic population from AI responses (#60)
- All fields populated, including attendees, samples, outcomes and follow-up actions (#72)

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

## Routing (#74)

- ✅ LLM intent routing with keyword fallback (ADR-004)
- ✅ Unsupported tool for greetings and unsupported requests
- ✅ Routing evaluation: LLM 47 / 47, keyword 32 / 47

## Edit Safety (#74)

- ✅ Only mentioned fields change
- ✅ Add / remove attendees, samples and products
- ✅ "Nothing to update" message
- ✅ Placeholder values stored as null

## Reliability (#69)

- ✅ Whole-word, priority-ordered intent routing
- ✅ Model `openai/gpt-oss-120b` (ADR-003)
- ✅ JSON Schema structured output
- ✅ Incomplete interaction guard
- ✅ Graceful error handling (no HTTP 500 from chat)
- ✅ Natural-language date resolution

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
- Five AI tools (plus an Unsupported fallback)
- LLM-based intent routing
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

Frontend Development

## ✅ Milestone 4

LangGraph Integration

## ✅ Milestone 5

AI Integration

## 🚧 Milestone 6

Deployment

## ⏳ Milestone 7

Testing & Demo

---

# Remaining Work

## Deployment

- Merge #66, tag v1.0.0, publish the GitHub release

## Improvements

- Conversation context ("she", "that meeting")
- Interaction history list in chat
- Frontend unit tests

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
| Version | v1.0.1 |
| Status | ✅ Closed — all milestones complete |
| Completed Issues | #1–#30, #58–#66, #69, #72, #74, #81 |
| Current Issue | — |
| Next Issue | — (see Follow-up Issues in `docs/issues/issue-progress.md`) |
| Active Branch | main |
| Model | openai/gpt-oss-120b |
| Routing | LLM + keyword fallback (47 / 47 on evaluation set) |
| Backend Tests | 281 (unit + database), live Groq tests opt-in |
| Database Migrations | 001 |
| Last Verified | 2026-10-20 — all 12 walkthrough screenshots captured; 281 passed, 55 skipped |
