from __future__ import annotations

from app.db.session import SessionLocal
from app.graph.state import CRMState
from app.graph.tools.serializers import serialize_interaction
from app.graph.tools.validation import require_hcp_name, resolve_hcp_name
from app.llm.groq import structured
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

    structured_llm = structured(
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
        
def history_response(hcp_name: str, interactions) -> str:
    """
    Summarise the history, including the latest interaction,
    so questions like "When did I last meet X?" are answered.

    Interactions are ordered newest first.
    """

    if not interactions:
        return f"No interactions found for {hcp_name}."

    latest = interactions[0]
    when = latest.interaction_date.strftime("%d-%m-%Y")
    channel = latest.channel.value.replace("_", " ").title()

    return (
        f"Retrieved {len(interactions)} interaction(s) for {hcp_name}. "
        f"Last interaction: {when} ({channel}) — {latest.summary}"
    )


def interaction_history(
    state: CRMState,
) -> CRMState:
    """
    LangGraph tool for retrieving interaction history.
    """

    extraction = extract_history(
        state["message"]
    )

    extraction.hcp_name = resolve_hcp_name(
        extraction.hcp_name,
        state["message"],
    )

    require_hcp_name(
        extraction.hcp_name,
        "Show my interactions with Alice Brown",
    )

    interactions = get_history_records(
        extraction
    )

    state["tool_input"] = extraction.model_dump()

    state["tool_output"] = {
        "success": True,
        "count": len(interactions),
        "hcp_name": extraction.hcp_name,
        "results": [
            serialize_interaction(interaction)
            for interaction in interactions
        ],
    }

    state["response"] = history_response(
        extraction.hcp_name,
        interactions,
    )

    return state