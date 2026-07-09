# AI-First CRM HCP Module

## Overview

AI-first CRM module for Healthcare Professionals (HCPs) built using FastAPI, React, PostgreSQL, LangGraph, and Groq.

## Tech Stack

### Frontend
- React
- Vite
- TypeScript
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

## Project Structure

```text
backend/
database/
docs/
frontend/
```

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## Backend Setup

```bash
cd backend

python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

pip install -r requirements.txt

uvicorn app.main:app --reload
```

API Documentation:

- http://127.0.0.1:8000/docs

Health Check:

- http://127.0.0.1:8000/health

## Database Setup

1. Install PostgreSQL.
2. Create a database named `ai_first_crm_hcp`.
3. Configure `backend/.env`.
4. Start the backend server.

## AI Setup

Create `backend/.env`:

```env
GROQ_API_KEY=your_api_key
MODEL_NAME=llama-3.3-70b-versatile
```

The project uses LangGraph with Groq as the LLM provider.

> **Note:** The original assignment specifies `gemma2-9b-it`. Since that model has been deprecated by Groq, this implementation uses `llama-3.3-70b-versatile`, a currently supported model, while keeping the overall architecture unchanged.

## Documentation

Project documentation is available under the `docs/` directory.

### Architecture

- System Architecture
- Backend Architecture
- Frontend Architecture
- Database Architecture
- LangGraph Architecture

### Architecture Decision Records

- ADR-001 — Project Structure

### Issue Tracking

- Issue Progress
- GitHub Project Board

## Project Verification

The following components have been verified:

- ✅ Frontend (React + Vite)
- ✅ Backend (FastAPI)
- ✅ PostgreSQL Connection
- ✅ LangGraph
- ✅ Groq Integration

## Current Status

- ✅ Project Setup
- 🚧 Backend Development
- 🚧 Frontend Development
- 🚧 LangGraph Integration