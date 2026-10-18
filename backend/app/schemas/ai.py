from __future__ import annotations

from typing import Literal

from pydantic import Field

from app.models.enums import InteractionChannel, Sentiment
from app.schemas.common import BaseSchema

# Field descriptions are included in the JSON schema sent to the LLM,
# so they double as extraction instructions.
HCP_NAME_DESCRIPTION = (
    "Name of the Healthcare Professional the request is about, "
    "without titles, e.g. 'Alice Brown' in 'my meeting with Dr. Alice "
    "Brown'. Never a product name. Null only if no person is named."
)
ATTENDEES_DESCRIPTION = (
    "Other people present besides the HCP and the representative, "
    "e.g. nurses or colleagues. Keep their titles exactly as written, "
    "e.g. 'Dr. Patel', 'Nurse Kelly'. Empty if none mentioned."
)
SAMPLES_DESCRIPTION = (
    "Product samples handed to the HCP. Empty if none mentioned."
)
OUTCOMES_DESCRIPTION = (
    "Agreements or results of the interaction, e.g. 'Agreed to "
    "trial Product A'. Null if none mentioned."
)
FOLLOW_UP_ACTIONS_DESCRIPTION = (
    "Concrete next steps for the representative, e.g. 'Send "
    "Phase III data'. Null if none mentioned."
)


class InteractionExtraction(BaseSchema):
    """
    Structured interaction information extracted by the LLM
    from a natural language conversation.

    This schema is used only by LangGraph tools and is
    independent of the database models.
    """

    hcp_name: str | None = Field(
        default=None,
        description=HCP_NAME_DESCRIPTION,
    )
    interaction_date: str
    channel: InteractionChannel
    raw_notes: str
    summary: str
    sentiment: Sentiment
    products_discussed: list[str] = []
    follow_up_required: bool = False
    follow_up_date: str | None = None
    attendees: list[str] = Field(
        default_factory=list,
        description=ATTENDEES_DESCRIPTION,
    )
    samples_distributed: list[str] = Field(
        default_factory=list,
        description=SAMPLES_DESCRIPTION,
    )
    outcomes: str | None = Field(
        default=None,
        description=OUTCOMES_DESCRIPTION,
    )
    follow_up_actions: str | None = Field(
        default=None,
        description=FOLLOW_UP_ACTIONS_DESCRIPTION,
    )


class InteractionUpdateExtraction(BaseSchema):
    """
    Structured interaction update extracted by the LLM.

    Only the fields that should be updated are populated.
    """

    hcp_name: str | None = Field(
        default=None,
        description=HCP_NAME_DESCRIPTION,
    )
    interaction_id: str | None = Field(
        default=None,
        description=(
            "ID of the interaction to edit, only if the user typed one "
            "(a UUID). Never invent an ID."
        ),
    )
    target_date: str | None = Field(
        default=None,
        description=(
            "Date of the EXISTING interaction the user wants to edit, "
            "e.g. '2026-10-15' for 'my meeting on 15 October'. Not the "
            "new value of a date being changed. Null if not mentioned."
        ),
    )

    interaction_date: str | None = None
    channel: InteractionChannel | None = None
    raw_notes: str | None = None
    summary: str | None = None
    sentiment: Sentiment | None = None
    products_discussed: list[str] | None = None
    follow_up_required: bool | None = None
    follow_up_date: str | None = None
    attendees: list[str] | None = Field(
        default=None,
        description=(
            "Only when the user gives the COMPLETE list of attendees. "
            + ATTENDEES_DESCRIPTION
        ),
    )
    samples_distributed: list[str] | None = Field(
        default=None,
        description=(
            "Only when the user gives the COMPLETE list of samples. "
            + SAMPLES_DESCRIPTION
        ),
    )
    outcomes: str | None = Field(
        default=None,
        description=OUTCOMES_DESCRIPTION,
    )
    follow_up_actions: str | None = Field(
        default=None,
        description=FOLLOW_UP_ACTIONS_DESCRIPTION,
    )

    # Incremental list changes ("add Dr. Patel", "remove Nurse Kelly").
    attendees_to_add: list[str] | None = Field(
        default=None,
        description="Attendees to add, keeping titles, e.g. ['Dr. Patel'].",
    )
    attendees_to_remove: list[str] | None = Field(
        default=None,
        description="Attendees to remove, e.g. ['Nurse Kelly'].",
    )
    samples_to_add: list[str] | None = Field(
        default=None,
        description="Samples to add to the samples distributed.",
    )
    samples_to_remove: list[str] | None = Field(
        default=None,
        description="Samples to remove from the samples distributed.",
    )
    products_to_add: list[str] | None = Field(
        default=None,
        description="Products to add to the products discussed.",
    )
    products_to_remove: list[str] | None = Field(
        default=None,
        description="Products to remove from the products discussed.",
    )


class HCPSearchExtraction(BaseSchema):
    """
    Structured Healthcare Professional search request
    extracted from natural language.
    """

    name: str | None = None
    specialization: str | None = None
    organization: str | None = None


class InteractionHistoryExtraction(BaseSchema):
    """
    Structured interaction history request extracted
    from natural language.
    """

    hcp_name: str | None = Field(
        default=None,
        description=HCP_NAME_DESCRIPTION,
    )
    limit: int | None = None


class FollowUpExtraction(BaseSchema):
    """
    Structured follow-up request extracted
    from natural language.
    """

    hcp_name: str | None = Field(
        default=None,
        description=HCP_NAME_DESCRIPTION,
    )


class FollowUpRecommendation(BaseSchema):
    """
    AI-generated follow-up recommendation.
    """

    recommendation: str
    rationale: str

IntentName = Literal[
    "log_interaction",
    "edit_interaction",
    "search_hcp",
    "interaction_history",
    "suggest_followup",
    "unsupported",
]


class IntentClassification(BaseSchema):
    """
    Tool selected by the LLM router for a user message.
    """

    tool: IntentName = Field(
        description="The single tool that should handle the message.",
    )
    reason: str = Field(
        default="",
        description="One short sentence explaining the choice.",
    )
