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

## Notes

The interaction form is intentionally read-only.

Users interact exclusively through the AI chat interface.

LangGraph uses a single graph architecture.

Five LangGraph tools will be implemented in later milestones.


## Current Snapshot

**Current Version:** v0.1.0

**Current Milestone:** Project Setup

**Completed Issues:** 1–6

**Current Issue:** #7 Project Documentation Foundation

**Next Issue:** #8 Verify Development Environment

**Active Branch:** feature/7-project-documentation-foundation