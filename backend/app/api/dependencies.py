from collections.abc import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.repositories.healthcare_professional import (
    HealthcareProfessionalRepository,
)
from app.services.healthcare_professional import (
    HealthcareProfessionalService,
)


def get_db() -> Generator[Session, None, None]:
    """Provide a database session."""

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def get_hcp_service(
    db: Session = Depends(get_db),
) -> HealthcareProfessionalService:
    """Provide the Healthcare Professional service."""

    repository = HealthcareProfessionalRepository(db)

    return HealthcareProfessionalService(repository)