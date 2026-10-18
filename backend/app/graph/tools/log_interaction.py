from __future__ import annotations

from datetime import datetime
from app.db.session import SessionLocal
from app.graph.state import CRMState
from app.graph.tools.serializers import serialize_interaction
from app.graph.tools.dates import date_rules, parse_date, parse_datetime
from app.llm.groq import structured
from app.repositories.healthcare_professional import (
    HealthcareProfessionalRepository,
)
from app.repositories.interaction import InteractionRepository
from app.schemas.ai import InteractionExtraction
from app.schemas.interaction import InteractionCreate
from app.services.healthcare_professional import (
    HealthcareProfessionalService,
)
from app.services.interaction import InteractionService


def extract_interaction(
    message: str,
) -> InteractionExtraction:
    """
    Extract structured interaction data from a
    natural language message.
    """

    structured_llm = structured(
        InteractionExtraction
    )
    prompt = f"""
    Extract the healthcare interaction.

    Rules:
    - Remove titles like Dr., Doctor, Prof., Mr., Mrs., and Ms. from the HCP name.
    - Never invent information. If the message does not name the HCP,
      return an empty string for hcp_name. Do the same for summary if
      nothing was discussed.
    - summary: a short summary of the topics discussed.
    - attendees: only other people present (not the HCP, not "I").
    - samples_distributed: only samples actually handed over.
    - outcomes: agreements or results; null if none.
    - follow_up_actions: next steps for the representative; null if none.
    {date_rules()}

    User Message:
    {message}
    """

    return structured_llm.invoke(prompt)


def create_interaction_record(
    extraction: InteractionExtraction,
):
    """
    Persist the extracted interaction.
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

        schema = InteractionCreate(
            hcp_id=hcp.id,
            interaction_date=(
                parse_datetime(extraction.interaction_date)
                or datetime.now()
            ),
            channel=extraction.channel,
            raw_notes=extraction.raw_notes,
            summary=extraction.summary,
            sentiment=extraction.sentiment,
            products_discussed=extraction.products_discussed,
            follow_up_required=extraction.follow_up_required,
            follow_up_date=parse_date(extraction.follow_up_date),
            attendees=extraction.attendees or None,
            samples_distributed=extraction.samples_distributed or None,
            outcomes=extraction.outcomes,
            follow_up_actions=extraction.follow_up_actions,
        )

        return interaction_service.create_interaction(
            schema
        )

    finally:
        db.close()
        
        
# Placeholders an LLM may return instead of leaving a field empty.
PLACEHOLDER_VALUES = {
    "unknown", "n/a", "na", "none", "null", "not specified",
    "not mentioned", "not provided", "unspecified", "-",
}


def is_missing(value: str | None) -> bool:
    """
    True when a required field is empty or only a placeholder.
    """

    if value is None:
        return True

    cleaned = value.strip().strip(".").lower()

    return not cleaned or cleaned in PLACEHOLDER_VALUES


def log_interaction(
    state: CRMState,
) -> CRMState:
    """
    LangGraph tool that logs an interaction.
    """

    extraction = extract_interaction(
        state["message"]
    )
    if (
        is_missing(extraction.hcp_name)
        or is_missing(extraction.interaction_date)
        or is_missing(extraction.summary)
    ):
        state["tool_input"] = extraction.model_dump()

        message = (
            "I couldn't identify a complete interaction. "
            "Please include the Healthcare Professional's name "
            "and interaction details."
        )

        state["tool_output"] = {
            "success": False,
            "error_type": "validation",
            "error": message,
            "reason": "Incomplete interaction information",
        }

        state["response"] = message

        return state

    interaction = create_interaction_record(
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
        f"Interaction logged successfully for "
        f"{extraction.hcp_name}."
    )

    return state
