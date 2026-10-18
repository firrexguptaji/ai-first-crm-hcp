"""
Explicit resolution of the interaction an edit should change (#81).

An edit is applied only when the target is unambiguous. Resolution
order, from most to least explicit:

1. Interaction ID in the message           ("interaction 3f2a…")
2. Date of the existing interaction        ("my meeting on 15 October")
3. Explicit "last / latest" reference      ("my last meeting with Alice Brown")
4. Interaction shown in the form           (sent by the frontend)
5. The HCP has exactly one interaction

Anything else raises ValueError with a clarification question,
so nothing is written to the database.
"""

from __future__ import annotations

import re
import uuid
from datetime import date
from typing import Protocol

from app.graph.tools.dates import parse_date
from app.models.interaction import Interaction

# "my last meeting", "the latest interaction", "my most recent visit"
LATEST_REFERENCE = re.compile(
    r"\b(?:my|the|our)\s+(?:last|latest|most\s+recent|previous)\s+"
    r"(?:interaction|meeting|visit|call|record|entry|conversation|chat)\b",
    re.IGNORECASE,
)

MAX_LISTED = 5


class InteractionLookup(Protocol):
    """Service methods needed for resolution."""

    def get_interaction(self, interaction_id: uuid.UUID) -> Interaction | None: ...

    def get_interaction_history(self, hcp_id, limit: int | None = None) -> list[Interaction]: ...


def _describe(interaction: Interaction) -> str:
    when = interaction.interaction_date.strftime("%d-%m-%Y")
    channel = interaction.channel.value.replace("_", " ").title()
    summary = interaction.summary or ""

    if len(summary) > 60:
        summary = summary[:57] + "..."

    return f"• {when} ({channel}) — {summary}"


def _clarify(hcp_name: str, interactions: list[Interaction], intro: str) -> ValueError:
    listed = "\n".join(_describe(i) for i in interactions[:MAX_LISTED])
    more = len(interactions) - MAX_LISTED

    if more > 0:
        listed += f"\n• … and {more} more"

    return ValueError(
        f"{intro}\n{listed}\n\n"
        "Which one should I update? Mention the date, e.g. "
        f"\"Change the sentiment of my meeting with {hcp_name} on "
        f"{interactions[0].interaction_date.strftime('%d-%m-%Y')} to positive\"."
    )


def _parse_id(value: str | None) -> uuid.UUID | None:
    if not value or not value.strip():
        return None

    try:
        return uuid.UUID(value.strip())
    except ValueError:
        raise ValueError(
            f"'{value}' is not a valid interaction ID."
        ) from None


def resolve_target_interaction(
    service: InteractionLookup,
    hcp,
    hcp_name: str,
    message: str,
    explicit_id: str | None = None,
    target_date: str | None = None,
    context_id: str | None = None,
    today: date | None = None,
) -> Interaction:
    """
    Return the interaction to edit, or raise ValueError asking
    the user to clarify. Never guesses.
    """

    # 1. Interaction ID named in the message
    interaction_uuid = _parse_id(explicit_id)

    if interaction_uuid is not None:
        interaction = service.get_interaction(interaction_uuid)

        if interaction is None or interaction.hcp_id != hcp.id:
            raise ValueError(
                f"I couldn't find interaction {interaction_uuid} for {hcp_name}."
            )

        return interaction

    history = service.get_interaction_history(hcp.id)

    if not history:
        raise ValueError(f"No interactions found for {hcp_name}.")

    # 2. Date of the existing interaction
    if target_date:
        day = parse_date(target_date, today=today)

        if day is None:
            raise ValueError(
                f"I couldn't understand which date you mean ('{target_date}')."
            )

        matches = [i for i in history if i.interaction_date.date() == day]

        if len(matches) == 1:
            return matches[0]

        if not matches:
            raise _clarify(
                hcp_name,
                history,
                f"I couldn't find an interaction with {hcp_name} on "
                f"{day.strftime('%d-%m-%Y')}. Their interactions are:",
            )

        raise _clarify(
            hcp_name,
            matches,
            f"{hcp_name} has {len(matches)} interactions on "
            f"{day.strftime('%d-%m-%Y')}:",
        )

    # 3. Explicit "my last meeting" (history is newest first)
    if LATEST_REFERENCE.search(message):
        return history[0]

    # 4. Interaction currently shown in the form
    context_uuid = None
    try:
        context_uuid = _parse_id(context_id)
    except ValueError:
        context_uuid = None

    if context_uuid is not None:
        for interaction in history:
            if interaction.id == context_uuid:
                return interaction

    # 5. Only one interaction
    if len(history) == 1:
        return history[0]

    raise _clarify(
        hcp_name,
        history,
        f"{hcp_name} has {len(history)} interactions:",
    )
