# Deployment Guide

## Overview

The application runs as three containers managed by Docker Compose:

```text
                    ┌──────────────────────────────────┐
Browser ──:8080───► │ frontend   nginx + React build   │
   │                └──────────────────────────────────┘
   │                ┌──────────────────────────────────┐
   └──────:8000───► │ backend    FastAPI + LangGraph   │ ───► Groq API
                    └────────────────┬─────────────────┘
                                     │ db:5432
                    ┌────────────────▼─────────────────┐
pgAdmin ──:5433───► │ db         PostgreSQL 16         │
                    │            volume: pgdata        │
                    └──────────────────────────────────┘
```

| Service | Image | Host Port | Health Check |
|---------|-------|-----------|--------------|
| `frontend` | `./frontend` (nginx) | 8080 | `GET /health` |
| `backend` | `./backend` (Python 3.12) | 8000 | `GET /health` |
| `db` | `postgres:16-alpine` | 5433 | `pg_isready` |

Start order: `db` → `backend` (after `db` is healthy) → `frontend` (after `backend` is healthy).

---

# Prerequisites

| Requirement | Notes |
|-------------|-------|
| Docker Desktop | Windows / macOS; Docker Engine + Compose plugin on Linux |
| Groq API key | https://console.groq.com |
| Free ports | 8080, 8000, 5433 |

Check:

```bash
docker --version
docker compose version
```

---

# Quick Start

```powershell
# 1. Configure
Copy-Item .env.example .env        # bash: cp .env.example .env
# Edit .env and set GROQ_API_KEY

# 2. Build and start
docker compose up --build
```

Wait for:

```text
backend-1  | Demo data inserted: 6 HCPs
backend-1  | INFO:     Application startup complete.
```

| What | URL |
|------|-----|
| App | http://localhost:8080 |
| API docs (Swagger) | http://localhost:8000/docs |
| Backend health | http://localhost:8000/health |
| Frontend health | http://localhost:8080/health |

Try in the chat:

```text
Met Alice Brown today at her clinic with Nurse Kelly. Discussed Product A, she was positive.
```

---

# Configuration

All settings live in `.env` in the project root (template: `.env.example`).

| Variable | Required | Default | Purpose |
|----------|----------|---------|---------|
| `GROQ_API_KEY` | Yes | — | Groq API key |
| `POSTGRES_USER` | No | `crm` | Database user |
| `POSTGRES_PASSWORD` | No | `crm_password` | Database password |
| `POSTGRES_DB` | No | `ai_first_crm_hcp` | Database name |
| `MODEL_NAME` | No | `openai/gpt-oss-120b` | Groq model |
| `ROUTER_MODE` | No | `llm` | `llm` (LLM routing, keyword fallback) or `keyword` |
| `SEED_DEMO_DATA` | No | `true` | Insert sample HCPs into an empty database |
| `VITE_API_URL` | No | `http://localhost:8000` | Backend URL as seen by the **browser**; baked into the frontend at build time |

Rules

- `.env` is git-ignored. Never commit it.
- Changing a backend setting: `docker compose up -d` (recreates the container).
- Changing `VITE_API_URL`: `docker compose up -d --build frontend` (needs a rebuild).
- Change `POSTGRES_*` **before** the first start. The database user is created only when the `pgdata` volume is empty.

---

# Daily Operations

| Task | Command |
|------|---------|
| Start in the background | `docker compose up -d` |
| Rebuild after code changes | `docker compose up -d --build` |
| Service status | `docker compose ps` |
| Follow backend logs | `docker compose logs -f backend` |
| Stop (keep data) | `docker compose down` |
| Stop and delete database | `docker compose down -v` |
| Seed demo data manually | `docker compose exec backend python -m app.db.seed` |
| Open a database shell | `docker compose exec db psql -U crm -d ai_first_crm_hcp` |

---

# Data

## Persistence

Data is stored in the `pgdata` Docker volume. It survives `docker compose down` and rebuilds, and is deleted only by `docker compose down -v`.

## Schema

Tables are created by the backend on startup (`create_all()`). A new Compose database always has the full schema, so migrations are **not** needed.

## Demo Data

Six sample HCPs (Alice Brown, John Smith, Priya Sharma, Rahul Mehta, Emily Clark, David Lee) are inserted only when the HCP table is empty. Existing data is never changed.

## Backup and Restore

```powershell
# Backup
docker compose exec -T db pg_dump -U crm ai_first_crm_hcp > backup.sql

# Restore into a running stack
Get-Content backup.sql | docker compose exec -T db psql -U crm -d ai_first_crm_hcp
```

## Reset for a Demo

```bash
docker compose down -v
docker compose up -d
```

---

# Running Without Compose

## Single Containers

```powershell
docker build -t ai-first-crm-backend ./backend
docker build -t ai-first-crm-frontend ./frontend

# Backend against PostgreSQL running on the host
$url = (Select-String -Path backend\.env -Pattern '^DATABASE_URL=').Line.Split('=', 2)[1].Replace('@localhost', '@host.docker.internal')
docker run --rm -p 8000:8000 --env-file backend/.env -e "DATABASE_URL=$url" ai-first-crm-backend

docker run --rm -p 8080:80 ai-first-crm-frontend
```

## Local Development

See the README section **Local Development** (`uvicorn` + `npm run dev`).

Databases created before #72 need migration 001:

```bash
psql -U postgres -d ai_first_crm_hcp -f database/migrations/001_add_interaction_fields.sql
```

---

# Deploying to a Server

The Compose stack runs on any Linux server with Docker.

```bash
git clone https://github.com/firrexguptaji/ai-first-crm-hcp.git
cd ai-first-crm-hcp
cp .env.example .env    # set GROQ_API_KEY and a strong POSTGRES_PASSWORD
```

Set `VITE_API_URL` to the backend URL users' browsers will call, for example `https://api.example.com`, then:

```bash
docker compose up -d --build
```

Before exposing it publicly

| Item | Action |
|------|--------|
| CORS | The backend allows `localhost` / `127.0.0.1` origins only. Add the public frontend origin in `backend/app/main.py`. |
| Database port | Remove the `5433:5432` mapping so PostgreSQL is not reachable from outside. |
| Passwords | Use a strong `POSTGRES_PASSWORD`. |
| HTTPS | Put a reverse proxy (Caddy, nginx, Traefik) with TLS in front of ports 8080 and 8000. |
| Authentication | The application has no user login. Do not expose it publicly without one. |

---

# Troubleshooting

Problems encountered during development and their fixes.

| Symptom | Cause | Fix |
|---------|-------|-----|
| `port is already allocated` | Local `uvicorn`, `npm run dev` or an older container uses the port | Stop it: `docker ps`, then `docker stop <name>` |
| `groq.AuthenticationError: 401 Invalid API Key` | `GROQ_API_KEY` in `.env` is still `your_groq_api_key` or wrong | Set the real key, then `docker compose up -d` |
| `Set GROQ_API_KEY in .env` when starting | `.env` missing or key empty | `Copy-Item .env.example .env` and set the key |
| `password authentication failed for user` | Wrong credentials, or `POSTGRES_*` changed after the volume was created | Use the original credentials, or reset: `docker compose down -v` |
| Single container: `connection refused` to `localhost:5432` | Inside a container, `localhost` is the container | Use `host.docker.internal` in `DATABASE_URL` |
| `Network is unreachable` (IPv6 address) next to another error | Docker tries IPv4 and IPv6 | Ignore it; read the IPv4 error |
| Chat shows "Can't reach the server" | Backend stopped or still starting | `docker compose ps`, `docker compose logs backend` |
| Chat shows "The AI is taking too long" | Slow Groq response (> 60 s) | Retry; check Groq status |
| `429` errors in backend logs | Groq rate limit | Wait a minute; slow down requests |
| `LLM routing failed, using keyword fallback` | Groq call failed (key, network, rate limit) | Fix the Groq error; the app keeps working with keyword routing |
| `column "attendees" does not exist` | Local database created before #72 | Run migration 001 |
| Browser CORS error from a new URL | Origin is not `localhost` / `127.0.0.1` | Add the origin in `backend/app/main.py` |
| Frontend calls the wrong backend URL | `VITE_API_URL` is fixed at build time | `docker compose up -d --build frontend` |
| Old UI after a rebuild | Browser cache | Hard refresh (Ctrl + F5); `index.html` is not cached by nginx |

## Useful Checks

```bash
docker compose ps                       # all services "healthy"?
docker compose logs --tail 50 backend   # recent backend errors
curl http://localhost:8000/health       # {"status":"ok"}
curl http://localhost:8080/health       # ok
```

---

# Related Documents

| Document | Content |
|----------|---------|
| `docs/architecture/backend.md` | Backend image, Compose services, demo data |
| `docs/architecture/frontend.md` | Frontend image, nginx configuration |
| `docs/architecture/database.md` | Schema, migrations, Compose database |
| `database/migrations/README.md` | Running SQL migrations |
