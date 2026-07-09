from __future__ import annotations

import uuid
from datetime import date, datetime

from app.models.healthcare_professional import HealthcareProfessional
from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import InteractionChannel, Sentiment


class Interaction(Base):
    """Interaction between a medical representative and a Healthcare Professional."""

    __tablename__ = "interactions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    hcp_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "healthcare_professionals.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    interaction_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    channel: Mapped[InteractionChannel] = mapped_column(
        Enum(InteractionChannel),
        nullable=False,
    )

    raw_notes: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    summary: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    sentiment: Mapped[Sentiment] = mapped_column(
        Enum(Sentiment),
        nullable=False,
    )

    products_discussed: Mapped[list[str] | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    follow_up_required: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    follow_up_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    hcp: Mapped["HealthcareProfessional"] = relationship(
        back_populates="interactions",
    )

    def __repr__(self) -> str:
        return (
            f"Interaction("
            f"id={self.id}, "
            f"hcp_id={self.hcp_id}, "
            f"interaction_date={self.interaction_date}"
            f")"
        )