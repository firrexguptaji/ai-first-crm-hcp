# Backend image for the AI-First CRM HCP API (#62)
#
# Build:  docker build -t ai-first-crm-backend ./backend
# Run:    docker run --env-file backend/.env -p 8000:8000 ai-first-crm-backend

FROM python:3.12-slim

# No .pyc files, unbuffered logs (visible immediately in `docker logs`).
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install dependencies first so this layer is cached
# when only application code changes.
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app ./app

# Run as a non-root user.
RUN useradd --create-home --uid 1000 appuser
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
