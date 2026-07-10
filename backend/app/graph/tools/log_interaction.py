from __future__ import annotations

from datetime import date, datetime, timedelta
from app.db.session import SessionLocal
from app.graph.state import CRMState
from app.llm.groq import llm
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

    structured_llm = llm.with_structured_output(
        InteractionExtraction
    )
    prompt = f"""
    Extract the healthcare interaction.

    Rules:
    - Remove titles like Dr., Doctor, Prof., Mr., Mrs., and Ms. from the HCP name.
    - interaction_date may be natural language such as "today" or "yesterday".
    - follow_up_date may be natural language such as "tomorrow" or "next week".

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
            interaction_date=parse_interaction_date(extraction.interaction_date),
            channel=extraction.channel,
            raw_notes=extraction.raw_notes,
            summary=extraction.summary,
            sentiment=extraction.sentiment,
            products_discussed=extraction.products_discussed,
            follow_up_required=extraction.follow_up_required,
            follow_up_date=parse_followup_date(extraction.follow_up_date),
        )

        return interaction_service.create_interaction(
            schema
        )

    finally:
        db.close()
        
        
def log_interaction(
    state: CRMState,
) -> CRMState:
    """
    LangGraph tool that logs an interaction.
    """

    extraction = extract_interaction(
        state["message"]
    )

    interaction = create_interaction_record(
        extraction
    )

    state["tool_input"] = extraction.model_dump()

    state["tool_output"] = {
        "success": True,
        "interaction_id": str(interaction.id),
    }

    state["response"] = (
        f"Interaction logged successfully for "
        f"{extraction.hcp_name}."
    )

    return state


def parse_interaction_date(value: str) -> datetime:
    """
    Convert natural language or ISO datetime into datetime.
    """

    value = value.strip().lower()

    if value == "today":
        return datetime.now()

    if value == "yesterday":
        return datetime.now() - timedelta(days=1)

    try:
        return datetime.fromisoformat(value)
    except ValueError:
        # Fallback if the LLM returns something unexpected
        return datetime.now()


def parse_followup_date(value: str | None) -> date | None:
    """
    Convert natural language or ISO date into date.
    """

    if value is None:
        return None

    value = value.strip().lower()

    if value == "today":
        return date.today()

    if value == "tomorrow":
        return date.today() + timedelta(days=1)

    if value == "next week":
        return date.today() + timedelta(days=7)

    try:
        return date.fromisoformat(value)
    except ValueError:
        return None
