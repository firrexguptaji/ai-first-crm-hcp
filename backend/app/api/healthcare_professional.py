from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_hcp_service
from app.schemas.healthcare_professional import (
    HealthcareProfessionalCreate,
    HealthcareProfessionalResponse,
    HealthcareProfessionalUpdate,
)
from app.services.healthcare_professional import (
    HealthcareProfessionalService,
)

router = APIRouter(
    prefix="/hcps",
    tags=["Healthcare Professionals"],
)


@router.post(
    "",
    response_model=HealthcareProfessionalResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_hcp(
    schema: HealthcareProfessionalCreate,
    service: HealthcareProfessionalService = Depends(get_hcp_service),
):
    """Create a new Healthcare Professional."""

    return service.create_hcp(schema)


@router.get(
    "",
    response_model=list[HealthcareProfessionalResponse],
)
def get_all_hcps(
    service: HealthcareProfessionalService = Depends(get_hcp_service),
):
    """Retrieve all Healthcare Professionals."""

    return service.get_all_hcps()


@router.get(
    "/{hcp_id}",
    response_model=HealthcareProfessionalResponse,
)
def get_hcp(
    hcp_id: UUID,
    service: HealthcareProfessionalService = Depends(get_hcp_service),
):
    """Retrieve a Healthcare Professional by ID."""

    hcp = service.get_hcp(hcp_id)

    if hcp is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Healthcare Professional not found.",
        )

    return hcp


@router.put(
    "/{hcp_id}",
    response_model=HealthcareProfessionalResponse,
)
def update_hcp(
    hcp_id: UUID,
    schema: HealthcareProfessionalUpdate,
    service: HealthcareProfessionalService = Depends(get_hcp_service),
):
    """Update a Healthcare Professional."""

    hcp = service.update_hcp(hcp_id, schema)

    if hcp is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Healthcare Professional not found.",
        )

    return hcp


@router.delete(
    "/{hcp_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_hcp(
    hcp_id: UUID,
    service: HealthcareProfessionalService = Depends(get_hcp_service),
):
    """Delete a Healthcare Professional."""

    deleted = service.delete_hcp(hcp_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Healthcare Professional not found.",
        )

    return None