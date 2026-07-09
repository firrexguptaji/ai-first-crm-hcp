from __future__ import annotations

from app.db.session import SessionLocal
from app.graph.state import CRMState
from app.llm.groq import llm
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

    structured_llm = llm.with_structured_output(
        InteractionUpdateExtraction
    )

    prompt = f"""
    Extract the requested updates for an existing
    healthcare interaction.

    User Message:
    {message}
    """

    return structured_llm.invoke(prompt)

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

        interaction = interaction_service.get_latest_interaction(
            hcp.id
        )

        if interaction is None:
            raise ValueError(
                "No interaction found."
            )

        schema = InteractionUpdate(
            interaction_date=extraction.interaction_date,
            channel=extraction.channel,
            raw_notes=extraction.raw_notes,
            summary=extraction.summary,
            sentiment=extraction.sentiment,
            products_discussed=extraction.products_discussed,
            follow_up_required=extraction.follow_up_required,
            follow_up_date=extraction.follow_up_date,
        )

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
    }

    state["response"] = (
        f"Interaction updated successfully for "
        f"{extraction.hcp_name}."
    )

    return state