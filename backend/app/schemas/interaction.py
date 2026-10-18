from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from app.models.enums import InteractionChannel, Sentiment
from app.schemas.common import BaseSchema


class InteractionBase(BaseSchema):
    """Shared Interaction fields."""

    hcp_id: UUID
    interaction_date: datetime
    channel: InteractionChannel
    raw_notes: str
    summary: str
    sentiment: Sentiment
    products_discussed: list[str] | None = None
    follow_up_required: bool = False
    follow_up_date: date | None = None
    attendees: list[str] | None = None
    samples_distributed: list[str] | None = None
    outcomes: str | None = None
    follow_up_actions: str | None = None


class InteractionCreate(InteractionBase):
    """Schema for creating an Interaction."""

    pass


class InteractionUpdate(BaseSchema):
    """Schema for updating an Interaction."""

    interaction_date: datetime | None = None
    channel: InteractionChannel | None = None
    raw_notes: str | None = None
    summary: str | None = None
    sentiment: Sentiment | None = None
    products_discussed: list[str] | None = None
    follow_up_required: bool | None = None
    follow_up_date: date | None = None
    attendees: list[str] | None = None
    samples_distributed: list[str] | None = None
    outcomes: str | None = None
    follow_up_actions: str | None = None


class InteractionResponse(InteractionBase):
    """Schema returned by the API."""

    id: UUID
    created_at: datetime
    updated_at: datetime