from fastapi import FastAPI

from app.api.healthcare_professional import router as hcp_router
from app.db.init_db import init_db

app = FastAPI(
    title="AI-First CRM HCP API",
    version="0.1.0",
)


@app.on_event("startup")
def startup():
    init_db()


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(hcp_router)