from __future__ import annotations

from app.db.session import SessionLocal
from app.graph.state import CRMState
from app.graph.tools.serializers import serialize_interaction
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
        - For list fields (attendees, samples_distributed,
          products_discussed), return the complete new list.
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


def build_update(
    extraction: InteractionUpdateExtraction,
) -> InteractionUpdate:
    """
    Convert the LLM extraction into an update schema.

    Natural-language dates are resolved here. A date the user
    asked to change but that cannot be understood raises
    ValueError, which the graph returns as a chat message.
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

    return InteractionUpdate(
        interaction_date=interaction_date,
        channel=extraction.channel,
        raw_notes=_provided(extraction.raw_notes),
        summary=_provided(extraction.summary),
        sentiment=extraction.sentiment,
        products_discussed=_provided(extraction.products_discussed),
        follow_up_required=extraction.follow_up_required,
        follow_up_date=follow_up_date,
        attendees=_provided(extraction.attendees),
        samples_distributed=_provided(extraction.samples_distributed),
        outcomes=_provided(extraction.outcomes),
        follow_up_actions=_provided(extraction.follow_up_actions),
    )


def update_interaction_record(
    extraction: InteractionUpdateExtraction,
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

        schema = build_update(extraction)

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

    interaction = update_interaction_record(
        extraction
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