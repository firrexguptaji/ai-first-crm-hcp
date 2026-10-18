from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.healthcare_professional import router as hcp_router
from app.api.interaction import router as interaction_router
from app.api.chat import router as chat_router
from app.config.settings import settings
from app.db.init_db import init_db
from app.db.seed import seed_demo_data

app = FastAPI(
    title="AI-First CRM HCP API",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    # Any local dev origin: localhost or 127.0.0.1 on any port
    # (Vite moves to 5174+ when 5173 is busy).
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()

    if settings.seed_demo_data:
        seed_demo_data()


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(hcp_router)
app.include_router(interaction_router)
app.include_router(chat_router)