from __future__ import annotations

from app.db.session import SessionLocal
from app.graph.state import CRMState
from app.llm.groq import llm
from app.repositories.healthcare_professional import (
    HealthcareProfessionalRepository,
)
from app.repositories.interaction import InteractionRepository
from app.schemas.ai import InteractionHistoryExtraction
from app.services.healthcare_professional import (
    HealthcareProfessionalService,
)
from app.services.interaction import InteractionService


def extract_history(
    message: str,
) -> InteractionHistoryExtraction:
    """
    Extract an interaction history request from
    natural language.
    """

    structured_llm = llm.with_structured_output(
        InteractionHistoryExtraction
    )

    prompt = f"""
    Extract the Healthcare Professional interaction
    history request.

    User Message:
    {message}
    """

    return structured_llm.invoke(prompt)

def get_history_records(
    extraction: InteractionHistoryExtraction,
):
    """
    Retrieve interaction history for a Healthcare Professional.
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

        return interaction_service.get_interaction_history(
            hcp_id=hcp.id,
            limit=extraction.limit,
        )

    finally:
        db.close()
        
def interaction_history(
    state: CRMState,
) -> CRMState:
    """
    LangGraph tool for retrieving interaction history.
    """

    extraction = extract_history(
        state["message"]
    )

    interactions = get_history_records(
        extraction
    )

    state["tool_input"] = extraction.model_dump()

    state["tool_output"] = {
        "success": True,
        "count": len(interactions),
        "results": [
            {
                "id": str(interaction.id),
                "interaction_date": interaction.interaction_date.isoformat(),
                "channel": interaction.channel.value,
                "summary": interaction.summary,
                "sentiment": interaction.sentiment.value,
                "follow_up_required": interaction.follow_up_required,
                "follow_up_date": (
                    interaction.follow_up_date.isoformat()
                    if interaction.follow_up_date
                    else None
                ),
            }
            for interaction in interactions
        ],
    }

    state["response"] = (
        f"Retrieved {len(interactions)} interaction(s) "
        f"for {extraction.hcp_name}."
    )

    return state