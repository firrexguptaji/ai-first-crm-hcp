from __future__ import annotations

from app.db.session import SessionLocal
from app.graph.state import CRMState
from app.llm.groq import llm
from app.repositories.healthcare_professional import (
    HealthcareProfessionalRepository,
)
from app.schemas.ai import HCPSearchExtraction
from app.services.healthcare_professional import (
    HealthcareProfessionalService,
)


def extract_search(
    message: str,
) -> HCPSearchExtraction:
    """
    Extract Healthcare Professional search criteria
    from a natural language request.
    """

    structured_llm = llm.with_structured_output(
        HCPSearchExtraction
    )

    prompt = f"""
    Extract the Healthcare Professional search criteria.

    Rules:
    - Remove titles like Dr., Doctor, Prof., Mr., Mrs., Ms.
    - Return only the person's actual name.
    - Do not include prefixes or honorifics.
    - If the user asks for specialization or organization, extract them.

    User Message:
    {message}
"""

    return structured_llm.invoke(prompt)

def search_hcp_records(
    extraction: HCPSearchExtraction,
):
    """
    Search Healthcare Professionals.
    """

    db = SessionLocal()

    try:
        service = HealthcareProfessionalService(
            HealthcareProfessionalRepository(db)
        )

        return service.search_hcps(
            name=extraction.name,
            specialization=extraction.specialization,
            organization=extraction.organization,
        )

    finally:
        db.close()
        
        
def search_hcp(
    state: CRMState,
) -> CRMState:
    """
    LangGraph tool for searching Healthcare
    Professionals.
    """

    extraction = extract_search(
        state["message"]
    )
    print(f"Extracted search criteria: {extraction}")

    hcps = search_hcp_records(
        extraction
    )

    state["tool_input"] = extraction.model_dump()

    state["tool_output"] = {
        "success": True,
        "count": len(hcps),
        "results": [
            {
                "id": str(hcp.id),
                "first_name": hcp.first_name,
                "last_name": hcp.last_name,
                "specialization": hcp.specialization,
                "organization": hcp.organization,
            }
            for hcp in hcps
        ],
    }

    state["response"] = (
        f"Found {len(hcps)} Healthcare Professional(s)."
    )

    return state