from uuid import UUID

from app.models.healthcare_professional import HealthcareProfessional
from app.repositories.healthcare_professional import (
    HealthcareProfessionalRepository,
)
from app.schemas.healthcare_professional import (
    HealthcareProfessionalCreate,
    HealthcareProfessionalUpdate,
)


class HealthcareProfessionalService:
    """Service layer for Healthcare Professional business logic."""

    def __init__(
        self,
        repository: HealthcareProfessionalRepository,
    ):
        self.repository = repository

    def create_hcp(
        self,
        schema: HealthcareProfessionalCreate,
    ) -> HealthcareProfessional:
        """Create a new Healthcare Professional."""

        hcp = HealthcareProfessional(**schema.model_dump())

        return self.repository.create(hcp)

    def get_hcp(
        self,
        hcp_id: UUID,
    ) -> HealthcareProfessional | None:
        """Retrieve a Healthcare Professional by ID."""

        return self.repository.get_by_id(hcp_id)

    def get_all_hcps(self) -> list[HealthcareProfessional]:
        """Retrieve all Healthcare Professionals."""

        return self.repository.get_all()

    def update_hcp(
        self,
        hcp_id: UUID,
        schema: HealthcareProfessionalUpdate,
    ) -> HealthcareProfessional | None:
        """Update an existing Healthcare Professional."""

        hcp = self.repository.get_by_id(hcp_id)

        if hcp is None:
            return None

        update_data = schema.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(hcp, field, value)

        return self.repository.update(hcp)

    def delete_hcp(
        self,
        hcp_id: UUID,
    ) -> bool:
        """Delete a Healthcare Professional."""

        hcp = self.repository.get_by_id(hcp_id)

        if hcp is None:
            return False

        self.repository.delete(hcp)

        return True
    
    def search_hcp_by_name(
    self,
    name: str,
    ):
        """
        Search a Healthcare Professional by name.
        """

        return self.repository.search_by_name(name)
    
    def search_hcps(
    self,
    name: str | None = None,
    specialization: str | None = None,
    organization: str | None = None,
    ):
        """
        Search Healthcare Professionals.
        """

        return self.repository.search(
            name=name,
            specialization=specialization,
            organization=organization,
        )