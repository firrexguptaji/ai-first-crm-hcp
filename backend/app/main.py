from fastapi import FastAPI
from sqlalchemy import text

from app.db.database import engine

app = FastAPI(
    title="AI-First CRM HCP API",
    version="0.1.0",
)


with engine.connect() as connection:
    connection.execute(text("SELECT 1"))

@app.get("/health")
def health_check():
    return {"status": "ok"}