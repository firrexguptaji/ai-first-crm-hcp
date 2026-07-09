from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import EmailStr

from app.schemas.common import BaseSchema


class HealthcareProfessionalBase(BaseSchema):
    """Shared Healthcare Professional fields."""

    first_name: str
    last_name: str
    specialization: str
    organization: str
    email: str | None = None
    phone: str | None = None


class HealthcareProfessionalCreate(HealthcareProfessionalBase):
    """Schema for creating a Healthcare Professional."""

    pass


class HealthcareProfessionalUpdate(BaseSchema):
    """Schema for updating a Healthcare Professional."""

    first_name: str | None = None
    last_name: str | None = None
    specialization: str | None = None
    organization: str | None = None
    email: str | None = None
    phone: str | None = None


class HealthcareProfessionalResponse(HealthcareProfessionalBase):
    """Schema returned by the API."""

    id: UUID
    created_at: datetime
    updated_at: datetime