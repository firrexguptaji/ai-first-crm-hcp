from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_interaction_service
from app.schemas.interaction import (
    InteractionCreate,
    InteractionResponse,
    InteractionUpdate,
)
from app.services.interaction import InteractionService

router = APIRouter(
    prefix="/interactions",
    tags=["Interactions"],
)


@router.post(
    "",
    response_model=InteractionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_interaction(
    schema: InteractionCreate,
    service: InteractionService = Depends(get_interaction_service),
):
    """Create a new Interaction."""

    return service.create_interaction(schema)


@router.get(
    "",
    response_model=list[InteractionResponse],
)
def get_all_interactions(
    service: InteractionService = Depends(get_interaction_service),
):
    """Retrieve all Interactions."""

    return service.repository.get_all()


@router.get(
    "/{interaction_id}",
    response_model=InteractionResponse,
)
def get_interaction(
    interaction_id: UUID,
    service: InteractionService = Depends(get_interaction_service),
):
    """Retrieve an Interaction by ID."""

    interaction = service.get_interaction(interaction_id)

    if interaction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interaction not found.",
        )

    return interaction


@router.put(
    "/{interaction_id}",
    response_model=InteractionResponse,
)
def update_interaction(
    interaction_id: UUID,
    schema: InteractionUpdate,
    service: InteractionService = Depends(get_interaction_service),
):
    """Update an Interaction."""

    interaction = service.update_interaction(
        interaction_id,
        schema,
    )

    if interaction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interaction not found.",
        )

    return interaction


@router.delete(
    "/{interaction_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_interaction(
    interaction_id: UUID,
    service: InteractionService = Depends(get_interaction_service),
):
    """Delete an Interaction."""

    deleted = service.delete_interaction(interaction_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interaction not found.",
        )

    return None