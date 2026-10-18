from __future__ import annotations

import logging
from datetime import datetime

from app.db.session import SessionLocal
from app.graph.state import CRMState
from app.graph.tools.serializers import serialize_interaction
from app.graph.tools.validation import (  # noqa: F401
    PLACEHOLDER_VALUES,
    clean_list,
    clean_text,
    is_missing,
)
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
    - Remove titles like Dr., Doctor, Prof., Mr., Mrs., and Ms. from hcp_name only.
    - Never invent information. If the message does not name the HCP,
      return an empty string for hcp_name. Do the same for summary if
      nothing was discussed.
    - summary: a short summary of the topics discussed.
    - attendees: only other people present (not the HCP, not "I").
      Keep their titles, e.g. "Dr. Patel", "Nurse Kelly".
    - samples_distributed: only samples actually handed over.
    - outcomes: agreements or results; null if none.
    - follow_up_actions: next steps for the representative; null if none.
    {date_rules()}

    User Message:
    {message}
    """

    return structured_llm.invoke(prompt)


def build_create(
    extraction: InteractionExtraction,
    hcp_id,
) -> InteractionCreate:
    """
    Convert the LLM extraction into a create schema.

    Optional fields are cleaned: empty values and placeholders
    such as "N/A" are stored as null.
    """

    return InteractionCreate(
        hcp_id=hcp_id,
        interaction_date=(
            parse_datetime(extraction.interaction_date)
            or datetime.now()
        ),
        channel=extraction.channel,
        raw_notes=extraction.raw_notes,
        summary=extraction.summary,
        sentiment=extraction.sentiment,
        products_discussed=clean_list(extraction.products_discussed),
        follow_up_required=extraction.follow_up_required,
        follow_up_date=parse_date(extraction.follow_up_date),
        attendees=clean_list(extraction.attendees),
        samples_distributed=clean_list(extraction.samples_distributed),
        outcomes=clean_text(extraction.outcomes),
        follow_up_actions=clean_text(extraction.follow_up_actions),
    )


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

        schema = build_create(extraction, hcp.id)

        return interaction_service.create_interaction(
            schema
        )

    finally:
        db.close()
        
        
logger = logging.getLogger(__name__)

# Required fields and how they are named in messages to the user.
REQUIRED_FIELDS = {
    "hcp_name": "Healthcare Professional name",
    "interaction_date": "interaction date",
    "summary": "topics discussed",
}


def log_interaction(
    state: CRMState,
) -> CRMState:
    """
    LangGraph tool that logs an interaction.
    """

    extraction = extract_interaction(
        state["message"]
    )
    missing = [
        label
        for field, label in REQUIRED_FIELDS.items()
        if is_missing(getattr(extraction, field))
    ]

    if missing:
        state["tool_input"] = extraction.model_dump()

        logger.warning(
            "Incomplete interaction, missing %s. Extraction: %s",
            missing,
            state["tool_input"],
        )

        message = (
            "I couldn't identify a complete interaction. "
            f"Missing: {', '.join(missing)}. "
            "Please include the Healthcare Professional's name "
            "and interaction details."
        )

        state["tool_output"] = {
            "success": False,
            "error_type": "validation",
            "error": message,
            "reason": "Incomplete interaction information",
            "missing": missing,
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
