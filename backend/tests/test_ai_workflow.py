from fastapi.testclient import TestClient
from app.db.session import SessionLocal
from app.repositories.healthcare_professional import (
    HealthcareProfessionalRepository,
)
from app.repositories.interaction import InteractionRepository
from app.services.healthcare_professional import (
    HealthcareProfessionalService,
)
from app.services.interaction import InteractionService
from app.main import app

client = TestClient(app)


def test_search_hcp_workflow():
    """
    Validate the complete Search HCP workflow.
    """

    response = client.post(
        "/chat",
        json={
            "message": "Find Alice Brown",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["tool_name"] == "search_hcp"
    assert "response" in body
    assert "tool_output" in body

    assert body["tool_output"]["success"] is True


def test_log_interaction_workflow():
    """
    Validate the complete Log Interaction workflow.
    """

    response = client.post(
        "/chat",
        json={
            "message": (
                "I met Alice Brown today. "
                "We discussed Product A. "
                "She requested additional clinical data. "
                "Schedule a follow-up next week."
            ),
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["tool_name"] == "log_interaction"
    assert body["tool_output"]["success"] is True


def test_interaction_history_workflow():
    """
    Validate the complete Interaction History workflow.
    """

    response = client.post(
        "/chat",
        json={
            "message": (
                "Show interaction history for Alice Brown"
            ),
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["tool_name"] == "interaction_history"
    assert body["tool_output"]["success"] is True


def test_suggest_followup_workflow():
    """
    Validate the complete Follow-up workflow.
    """

    response = client.post(
        "/chat",
        json={
            "message": (
                "Suggest a follow-up for Alice Brown"
            ),
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["tool_name"] == "suggest_followup"
    assert body["tool_output"]["success"] is True
    
    
def test_log_interaction_persists_to_database():
    """
    Validate that a logged interaction is stored
    in the database.
    """

    client.post(
        "/chat",
        json={
            "message": (
                "I met Alice Brown today. "
                "We discussed Product A. "
                "She requested additional clinical data."
            )
        },
    )

    db = SessionLocal()

    try:
        hcp_service = HealthcareProfessionalService(
            HealthcareProfessionalRepository(db)
        )

        interaction_service = InteractionService(
            InteractionRepository(db)
        )

        hcp = hcp_service.search_hcp_by_name(
            "Alice Brown"
        )

        assert hcp is not None

        history = interaction_service.get_interaction_history(
            hcp.id
        )

        assert len(history) > 0

    finally:
        db.close()
        
def test_edit_interaction_updates_database():
    """
    Validate that editing an interaction
    updates the persisted record.
    """

    client.post(
        "/chat",
        json={
            "message": (
                "Update the latest interaction with Alice Brown. "
                "Change the summary to "
                "'Requested updated efficacy data.'"
            )
        },
    )

    db = SessionLocal()

    try:
        hcp_service = HealthcareProfessionalService(
            HealthcareProfessionalRepository(db)
        )

        interaction_service = InteractionService(
            InteractionRepository(db)
        )

        hcp = hcp_service.search_hcp_by_name(
            "Alice Brown"
        )

        interaction = (
            interaction_service.get_latest_interaction(
                hcp.id
            )
        )

        assert interaction is not None

        assert (
            interaction.summary
            == "Requested updated efficacy data."
        )

    finally:
        db.close()