from __future__ import annotations

from app.db.session import SessionLocal
from app.graph.state import CRMState
from app.llm.groq import llm
from app.repositories.healthcare_professional import (
    HealthcareProfessionalRepository,
)
from app.repositories.interaction import InteractionRepository
from app.schemas.ai import (
    FollowUpExtraction,
    FollowUpRecommendation,
)
from app.services.healthcare_professional import (
    HealthcareProfessionalService,
)
from app.services.interaction import InteractionService

def extract_followup(
    message: str,
) -> FollowUpExtraction:
    """
    Extract the Healthcare Professional
    from the user's request.
    """

    structured_llm = llm.with_structured_output(
        FollowUpExtraction
    )

    prompt = f"""
    Extract the Healthcare Professional name.

    User Message:
    {message}
    """

    return structured_llm.invoke(prompt)

def generate_followup(
    extraction: FollowUpExtraction,
) -> FollowUpRecommendation:
    """
    Generate an AI follow-up recommendation.
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

        latest = interaction_service.get_latest_interaction(
            hcp.id
        )

        history = interaction_service.get_interaction_history(
            hcp.id
        )

        structured_llm = llm.with_structured_output(
            FollowUpRecommendation
        )

        prompt = f"""
        You are assisting a pharmaceutical CRM.

    Healthcare Professional:
    {hcp.first_name} {hcp.last_name}

    Latest Interaction:
    {latest.summary if latest else 'None'}

    Previous Interactions:
    {[interaction.summary for interaction in history]}

    Generate one follow-up recommendation and explain why.
    """

        return structured_llm.invoke(prompt)

    finally:
        db.close()
        
        
def suggest_followup(
    state: CRMState,
) -> CRMState:
    """
    LangGraph tool for generating
    follow-up recommendations.
    """

    extraction = extract_followup(
        state["message"]
    )

    recommendation = generate_followup(
        extraction
    )

    state["tool_input"] = extraction.model_dump()

    state["tool_output"] = {
        "success": True,
        "recommendation": recommendation.model_dump(),
    }

    state["response"] = recommendation.recommendation

    return state