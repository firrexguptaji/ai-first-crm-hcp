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

from app.repositories.interaction import InteractionRepository
from app.services.interaction import InteractionService

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

def get_interaction_service(
    db: Session = Depends(get_db),
) -> InteractionService:
    """Provide the Interaction service."""

    repository = InteractionRepository(db)

    return InteractionService(repository)