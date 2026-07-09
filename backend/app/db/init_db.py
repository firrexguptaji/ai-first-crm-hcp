from app.db.base import Base
import app.models

from app.db.database import engine


def init_db() -> None:
    """Create all database tables."""

    Base.metadata.create_all(bind=engine)