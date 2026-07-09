# AI-First CRM HCP — Project Context

## Project Overview

**Project:** AI-First CRM HCP Module

**Purpose**

Build an AI-first CRM module for Healthcare Professionals where all interaction data is managed through an AI assistant powered by LangGraph.

This project is being developed as a production-style technical assignment using issue-driven development.

---

## Tech Stack

### Frontend

- React
- TypeScript
- Vite
- Redux Toolkit

### Backend

- FastAPI
- SQLAlchemy
- PostgreSQL

### AI

- LangGraph
- LangChain
- Groq
- Model: llama-3.3-70b-versatile

---

## Engineering Principles

- One Issue = One Feature
- One Feature = One Pull Request
- Documentation updated after every completed issue
- ADRs for significant architectural decisions
- Simplicity over unnecessary complexity
- Stay within assignment scope

---

## Current Project Status

Current Milestone:

Project Setup

Completed Issues:

- #1 Initialize Repository Structure
- #2 Configure GitHub Project Management
- #3 Initialize Frontend
- #4 Initialize Backend
- #5 Configure PostgreSQL & SQLAlchemy
- #6 Configure LangGraph & Groq

Current Issue:

#7 Project Documentation Foundation

Next Issue:

#8 Verify Development Environment

---

## Repository Structure

```text
backend/
database/
docs/
frontend/
README.md
```

---

## Git Workflow

Issue

↓

Feature Branch

↓

Implementation

↓

Testing

↓

Documentation

↓

Commit

↓

Pull Request

↓

Merge

↓

Close Issue

---

## Architecture Summary

Frontend (React)

↓

FastAPI

↓

LangGraph

↓

Groq

↓

PostgreSQL

---

## Backend Status

### Completed

- FastAPI initialized
- PostgreSQL configured
- SQLAlchemy configured
- Database schema designed
- SQLAlchemy models implemented
- Pydantic schemas
- Repository layer
- Service layer
- Healthcare Professional API
- Interaction API

### Pending

- LangGraph Tools
- AI Workflow

## Frontend Status

### Completed

- React initialized
- Vite configured
- TypeScript configured

### Pending

- Layout
- Redux Toolkit
- Read-only interaction form
- AI chat
- API integration

## AI Status

### Completed

- LangGraph configured
- Groq configured
- Base graph implemented
- Graph invocation verified

### Pending

- Graph routing
- Log Interaction Tool
- Edit Interaction Tool
- Search HCP Tool
- Interaction History Tool
- Follow-up Suggestion Tool
## Database Status

Current Entities

- HealthcareProfessional
- Interaction

Relationship

HealthcareProfessional (1)

↓

Interaction (Many)

Current State

- Schema designed
- ORM models implemented

Pending

- Alembic migrations
- Repository layer



## Assignment Constraints

- Read-only interaction form
- All updates performed through AI chat
- Minimum two mandatory LangGraph tools
- Total of five LangGraph tools planned
- Keep architecture simple
- Avoid multi-agent workflows unless required

## Notes

The interaction form is intentionally read-only.

Users interact exclusively through the AI chat interface.

LangGraph uses a single graph architecture.

Five LangGraph tools will be implemented in later milestones.


## Current Snapshot

| Item | Value |
|------|-------|
| Version | v0.2.3 |
| Milestone | LangGraph Integration |
| Completed Issues | #1–#15, #23–#26 |
| Current Issue | #27 Implement Retrieve Interaction History Tool |
| Next Issue | #28 Implement Follow-up Suggestion Tool |
| Active Branch | feature/27-retrieve-interaction-history |
| Last Verified | Implement Search HCP Tool |