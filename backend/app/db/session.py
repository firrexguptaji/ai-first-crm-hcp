from sqlalchemy.orm import sessionmaker

from app.db.database import engine

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)