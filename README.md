# AI-First CRM HCP Module

An AI-first CRM module for Healthcare Professionals (HCPs) built as part of a technical assignment.

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
- Groq (gemma2-9b-it)

## Project Structure

```text
backend/
frontend/
database/
docs/
```

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The development server runs at:

http://localhost:5173

## Backend Setup

```bash
cd backend

python -m venv .venv

# Activate the virtual environment (PowerShell)
.venv\Scripts\Activate.ps1

pip install -r requirements.txt

uvicorn app.main:app --reload
```

API Documentation:

- http://127.0.0.1:8000/docs

Health Check:

- http://127.0.0.1:8000/health

## Project Status

🚧 Under Development