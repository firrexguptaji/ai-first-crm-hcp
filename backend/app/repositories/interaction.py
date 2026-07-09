from uuid import UUID

from sqlalchemy.orm import Session

from app.models.interaction import Interaction


class InteractionRepository:
    """Repository for Interaction database operations."""

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        interaction: Interaction,
    ) -> Interaction:
        """Create a new Interaction."""

        self.db.add(interaction)
        self.db.commit()
        self.db.refresh(interaction)
        return interaction

    def get_by_id(
        self,
        interaction_id: UUID,
    ) -> Interaction | None:
        """Retrieve an Interaction by ID."""

        return (
            self.db.query(Interaction)
            .filter(Interaction.id == interaction_id)
            .first()
        )

    def get_by_hcp(
        self,
        hcp_id: UUID,
    ) -> list[Interaction]:
        """Retrieve all Interactions for a Healthcare Professional."""

        return (
            self.db.query(Interaction)
            .filter(Interaction.hcp_id == hcp_id)
            .all()
        )

    def get_all(self) -> list[Interaction]:
        """Retrieve all Interactions."""

        return self.db.query(Interaction).all()

    def update(
        self,
        interaction: Interaction,
    ) -> Interaction:
        """Update an existing Interaction."""

        self.db.commit()
        self.db.refresh(interaction)
        return interaction

    def delete(
        self,
        interaction: Interaction,
    ) -> None:
        """Delete an Interaction."""

        self.db.delete(interaction)
        self.db.commit()
        
        
    def get_latest_by_hcp(
    self,
    hcp_id: UUID,
    ) -> Interaction | None:
        """
        Retrieve the most recent interaction for
        a Healthcare Professional.
        """

        return (
            self.db.query(Interaction)
            .filter(Interaction.hcp_id == hcp_id)
            .order_by(Interaction.interaction_date.desc())
            .first()
        )
        
    def get_latest_interaction(
        self,
        hcp_id,
    ):
        """
        Retrieve the latest interaction for an HCP.
        """

        return self.repository.get_latest_by_hcp(hcp_id)
    
    def get_history_by_hcp(
    self,
    hcp_id: UUID,
    limit: int | None = None,
    ) -> list[Interaction]:
        """
        Retrieve interaction history for a Healthcare Professional.

        Results are returned in reverse chronological order.
        """

        query = (
            self.db.query(Interaction)
            .filter(Interaction.hcp_id == hcp_id)
            .order_by(Interaction.interaction_date.desc())
        )

        if limit is not None:
            query = query.limit(limit)

        return query.all()