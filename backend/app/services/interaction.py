from uuid import UUID

from app.models.interaction import Interaction
from app.repositories.interaction import InteractionRepository
from app.schemas.interaction import (
    InteractionCreate,
    InteractionUpdate,
)


class InteractionService:
    """Service layer for Interaction business logic."""

    def __init__(
        self,
        repository: InteractionRepository,
    ):
        self.repository = repository

    def create_interaction(
        self,
        schema: InteractionCreate,
    ) -> Interaction:
        """Create a new Interaction."""

        interaction = Interaction(**schema.model_dump())

        return self.repository.create(interaction)

    def get_interaction(
        self,
        interaction_id: UUID,
    ) -> Interaction | None:
        """Retrieve an Interaction by ID."""

        return self.repository.get_by_id(interaction_id)

    def get_hcp_interactions(
        self,
        hcp_id: UUID,
    ) -> list[Interaction]:
        """Retrieve all Interactions for a Healthcare Professional."""

        return self.repository.get_by_hcp(hcp_id)

    def update_interaction(
        self,
        interaction_id: UUID,
        schema: InteractionUpdate,
    ) -> Interaction | None:
        """Update an existing Interaction."""

        interaction = self.repository.get_by_id(interaction_id)

        if interaction is None:
            return None

        update_data = schema.model_dump(
            exclude_unset=True,
            exclude_none=True,)

        for field, value in update_data.items():
            setattr(interaction, field, value)

        return self.repository.update(interaction)

    def delete_interaction(
        self,
        interaction_id: UUID,
    ) -> bool:
        """Delete an Interaction."""

        interaction = self.repository.get_by_id(interaction_id)

        if interaction is None:
            return False

        self.repository.delete(interaction)

        return True
    def get_interaction_history(
    self,
    hcp_id,
    limit: int | None = None,
    ):
        """
        Retrieve the interaction history for a Healthcare Professional.
        """

        return self.repository.get_history_by_hcp(
            hcp_id=hcp_id,
            limit=limit,
        )
        
    def get_latest_interaction(
    self,
    hcp_id: UUID,
    ) -> Interaction | None:
        """
        Retrieve the latest interaction for a Healthcare Professional.
        """

        return self.repository.get_latest_by_hcp(hcp_id)