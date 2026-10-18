"""
Convert ORM objects into JSON-safe dictionaries for tool output.

The frontend uses these dictionaries to populate the
Interaction Details form, so every tool that returns an
interaction uses the same shape.
"""

from __future__ import annotations

from typing import Any

from app.models.interaction import Interaction


def serialize_interaction(interaction: Interaction) -> dict[str, Any]:
    """
    Serialize an Interaction for tool output.
    """

    return {
        "id": str(interaction.id),
        "hcp_id": str(interaction.hcp_id),
        "interaction_date": interaction.interaction_date.isoformat(),
        "channel": interaction.channel.value,
        "raw_notes": interaction.raw_notes,
        "summary": interaction.summary,
        "sentiment": interaction.sentiment.value,
        "products_discussed": interaction.products_discussed or [],
        "follow_up_required": interaction.follow_up_required,
        "follow_up_date": (
            interaction.follow_up_date.isoformat()
            if interaction.follow_up_date
            else None
        ),
    }
