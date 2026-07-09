from uuid import UUID

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.healthcare_professional import HealthcareProfessional


class HealthcareProfessionalRepository:
    """Repository for Healthcare Professional database operations."""

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        hcp: HealthcareProfessional,
    ) -> HealthcareProfessional:
        """Create a new Healthcare Professional."""

        self.db.add(hcp)
        self.db.commit()
        self.db.refresh(hcp)
        return hcp

    def get_by_id(
        self,
        hcp_id: UUID,
    ) -> HealthcareProfessional | None:
        """Retrieve a Healthcare Professional by ID."""

        return (
            self.db.query(HealthcareProfessional)
            .filter(HealthcareProfessional.id == hcp_id)
            .first()
        )

    def get_all(self) -> list[HealthcareProfessional]:
        """Retrieve all Healthcare Professionals."""

        return self.db.query(HealthcareProfessional).all()

    def get_by_email(
        self,
        email: str,
    ) -> HealthcareProfessional | None:
        """Retrieve a Healthcare Professional by email."""

        return (
            self.db.query(HealthcareProfessional)
            .filter(HealthcareProfessional.email == email)
            .first()
        )

    def update(
        self,
        hcp: HealthcareProfessional,
    ) -> HealthcareProfessional:
        """Update an existing Healthcare Professional."""

        self.db.commit()
        self.db.refresh(hcp)
        return hcp

    def delete(
        self,
        hcp: HealthcareProfessional,
    ) -> None:
        """Delete a Healthcare Professional."""

        self.db.delete(hcp)
        self.db.commit()

    def search_by_name(
        self,
        name: str,
    ) -> HealthcareProfessional | None:
        """
        Find a Healthcare Professional by name.
        """

        search = f"%{name}%"

        return (
            self.db.query(HealthcareProfessional)
            .filter(
                or_(
                    HealthcareProfessional.first_name.ilike(search),
                    HealthcareProfessional.last_name.ilike(search),
                )
            )
            .first()
        )

    def search(
        self,
        name: str | None = None,
        specialization: str | None = None,
        organization: str | None = None,
    ) -> list[HealthcareProfessional]:
        """
        Search Healthcare Professionals using optional filters.
        """

        query = self.db.query(HealthcareProfessional)

        if name:
            search = f"%{name}%"

            query = query.filter(
                or_(
                    HealthcareProfessional.first_name.ilike(search),
                    HealthcareProfessional.last_name.ilike(search),
                )
            )

        if specialization:
            query = query.filter(
                HealthcareProfessional.specialization.ilike(
                    f"%{specialization}%"
                )
            )

        if organization:
            query = query.filter(
                HealthcareProfessional.organization.ilike(
                    f"%{organization}%"
                )
            )

        return query.all()