from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class HealthcareProfessional(Base):
    """Healthcare Professional (HCP) model."""

    __tablename__ = "healthcare_professionals"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    specialization: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    organization: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    email: Mapped[str | None] = mapped_column(
        String(255),
        unique=True,
        nullable=True,
    )

    phone: Mapped[str | None] = mapped_column(
        String(30),
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

    interactions: Mapped[list["Interaction"]] = relationship(
        back_populates="hcp",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return (
            f"HealthcareProfessional("
            f"id={self.id}, "
            f"name='{self.first_name} {self.last_name}'"
            f")"
        )