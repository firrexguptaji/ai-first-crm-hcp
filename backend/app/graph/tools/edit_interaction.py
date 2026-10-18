from __future__ import annotations

from app.db.session import SessionLocal
from app.graph.state import CRMState
from app.graph.tools.serializers import serialize_interaction
from app.graph.tools.validation import mentions, require_hcp_name, resolve_hcp_name
from app.graph.tools.dates import date_rules, parse_date, parse_datetime
from app.llm.groq import structured
from app.repositories.healthcare_professional import (
    HealthcareProfessionalRepository,
)
from app.repositories.interaction import InteractionRepository
from app.schemas.ai import InteractionUpdateExtraction
from app.schemas.interaction import InteractionUpdate
from app.services.healthcare_professional import (
    HealthcareProfessionalService,
)
from app.services.interaction import InteractionService


def extract_update(
    message: str,
) -> InteractionUpdateExtraction:
    """
    Extract an interaction update request from
    natural language.
    """

    structured_llm = structured(
        InteractionUpdateExtraction
    )

    prompt = f"""
        Extract the requested updates for an existing
        healthcare interaction.

        Rules:
        - Remove titles like Dr., Doctor, Prof., Mr., Mrs., and Ms. from hcp_name only.
        - Keep titles in attendees, e.g. "Dr. Patel", "Nurse Kelly".
        - Only populate fields that the user wants to update.
          Leave every other field null. Never return empty strings
          or empty lists for fields the user did not mention.
        - To add or remove single attendees, samples or products, use
          attendees_to_add / attendees_to_remove, samples_to_add /
          samples_to_remove, products_to_add / products_to_remove.
          Use attendees, samples_distributed or products_discussed
          only when the user gives the complete new list.
        {date_rules()}

        User Message:
        {message}
    """

    return structured_llm.invoke(prompt)

def _provided(value):
    """
    Return None for values the user did not ask to change.

    The LLM sometimes returns "" or [] for fields that were not
    mentioned instead of leaving them out. Saving those would wipe
    existing data, so empty values are treated as "not provided".
    """

    if value is None:
        return None

    if isinstance(value, str) and not value.strip():
        return None

    if isinstance(value, list) and not value:
        return None

    return value


# Fields that LLMs tend to fill with a default value. They are only
# applied when the message actually talks about them.
SENTIMENT_WORDS = (
    "sentiment", "positive", "negative", "neutral", "happy", "unhappy",
    "pleased", "satisfied", "dissatisfied", "receptive", "skeptical",
    "sceptical", "enthusiastic", "interested", "uninterested", "upset",
    "annoyed", "frustrated", "mood", "felt", "feel", "liked", "disliked",
)
CHANNEL_WORDS = (
    "channel", "call", "called", "phone", "telephone", "email", "e-mail",
    "emailed", "video", "zoom", "teams", "virtual", "online", "in person",
    "in-person", "face to face", "face-to-face",
)
FOLLOW_UP_WORDS = ("follow", "follow-up", "followup", "follow up")

NOTHING_TO_UPDATE_MESSAGE = (
    "I couldn't tell what to change. Please say which field to "
    "update, e.g. \"Change the sentiment for Alice Brown to positive\" "
    "or \"Add Dr. Patel as an attendee for Alice Brown\"."
)


def _matches(item: str, name: str) -> bool:
    """
    Loose match for removals: "Kelly" matches "Nurse Kelly".
    """

    a, b = item.strip().lower(), name.strip().lower()

    return bool(a and b) and (a in b or b in a)


def merge_list(
    current: list[str] | None,
    replacement: list[str] | None,
    to_add: list[str] | None,
    to_remove: list[str] | None,
) -> list[str] | None:
    """
    Apply list changes to the current values.

    Returns None when the list does not change.
    """

    replacement = _provided(replacement)
    to_add = _provided(to_add) or []
    to_remove = _provided(to_remove) or []

    if replacement is None and not to_add and not to_remove:
        return None

    result = list(replacement if replacement is not None else (current or []))

    for item in to_add:
        if not any(existing.lower() == item.lower() for existing in result):
            result.append(item)

    result = [
        existing for existing in result
        if not any(_matches(existing, name) for name in to_remove)
    ]

    if result == (current or []):
        return None

    return result


def build_update(
    extraction: InteractionUpdateExtraction,
    message: str | None = None,
    current=None,
) -> InteractionUpdate:
    """
    Convert the LLM extraction into an update schema.

    - Natural-language dates are resolved; unreadable dates raise
      ValueError, which the graph returns as a chat message.
    - Sentiment, channel and the follow-up flag are applied only when
      the message mentions them (when `message` is given), so LLM
      defaults never overwrite stored values.
    - List fields support add / remove relative to `current`
      (the interaction being edited).
    """

    interaction_date = parse_datetime(extraction.interaction_date)
    if extraction.interaction_date and interaction_date is None:
        raise ValueError(
            f"I couldn't understand the interaction date "
            f"'{extraction.interaction_date}'. "
            "Please use a date like 2026-10-18 or 'yesterday'."
        )

    follow_up_date = parse_date(extraction.follow_up_date)
    if extraction.follow_up_date and follow_up_date is None:
        raise ValueError(
            f"I couldn't understand the follow-up date "
            f"'{extraction.follow_up_date}'. "
            "Please use a date like 2026-10-25 or 'next week'."
        )

    sentiment = extraction.sentiment
    channel = extraction.channel
    follow_up_required = extraction.follow_up_required

    if message is not None:
        if not mentions(message, SENTIMENT_WORDS):
            sentiment = None
        if not mentions(message, CHANNEL_WORDS):
            channel = None
        if not mentions(message, FOLLOW_UP_WORDS):
            follow_up_required = None

    # Setting a follow-up date implies a follow-up is required.
    if follow_up_date is not None and follow_up_required is None:
        follow_up_required = True

    return InteractionUpdate(
        interaction_date=interaction_date,
        channel=channel,
        raw_notes=_provided(extraction.raw_notes),
        summary=_provided(extraction.summary),
        sentiment=sentiment,
        products_discussed=merge_list(
            getattr(current, "products_discussed", None),
            extraction.products_discussed,
            extraction.products_to_add,
            extraction.products_to_remove,
        ),
        follow_up_required=follow_up_required,
        follow_up_date=follow_up_date,
        attendees=merge_list(
            getattr(current, "attendees", None),
            extraction.attendees,
            extraction.attendees_to_add,
            extraction.attendees_to_remove,
        ),
        samples_distributed=merge_list(
            getattr(current, "samples_distributed", None),
            extraction.samples_distributed,
            extraction.samples_to_add,
            extraction.samples_to_remove,
        ),
        outcomes=_provided(extraction.outcomes),
        follow_up_actions=_provided(extraction.follow_up_actions),
    )


def update_interaction_record(
    extraction: InteractionUpdateExtraction,
    message: str | None = None,
):
    """
    Update an existing interaction.
    """

    db = SessionLocal()

    try:
        hcp_service = HealthcareProfessionalService(
            HealthcareProfessionalRepository(db)
        )

        interaction_service = InteractionService(
            InteractionRepository(db)
        )

        hcp = hcp_service.search_hcp_by_name(
            extraction.hcp_name
        )

        if hcp is None:
            raise ValueError(
                f"HCP '{extraction.hcp_name}' not found."
            )

        # The interaction the user most recently recorded,
        # i.e. the one shown in the form after logging.
        interaction = interaction_service.get_last_recorded_interaction(
            hcp.id
        )

        if interaction is None:
            raise ValueError(
                "No interaction found."
            )

        schema = build_update(extraction, message, interaction)

        if not schema.model_dump(exclude_none=True):
            raise ValueError(NOTHING_TO_UPDATE_MESSAGE)

        return interaction_service.update_interaction(
            interaction.id,
            schema,
        )

    finally:
        db.close()
        
        
def edit_interaction(
    state: CRMState,
) -> CRMState:
    """
    LangGraph tool for updating an existing
    interaction.
    """

    extraction = extract_update(
        state["message"]
    )

    extraction.hcp_name = resolve_hcp_name(
        extraction.hcp_name,
        state["message"],
    )

    require_hcp_name(
        extraction.hcp_name,
        "Change the sentiment for Alice Brown to negative",
    )

    interaction = update_interaction_record(
        extraction,
        state["message"],
    )

    state["tool_input"] = extraction.model_dump()

    state["tool_output"] = {
        "success": True,
        "interaction_id": str(interaction.id),
        "hcp_name": extraction.hcp_name,
        "interaction": serialize_interaction(interaction),
    }

    state["response"] = (
        f"Interaction updated successfully for "
        f"{extraction.hcp_name}."
    )

    return state