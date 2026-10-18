"""
End-to-end /chat behaviour against a real database (#81, P1).
LLM routing and extraction are replaced with fixed values.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.interaction import Interaction
from app.schemas.ai import InteractionExtraction
from app.models.enums import InteractionChannel, Sentiment

pytestmark = pytest.mark.db

client = TestClient(app)


@pytest.fixture
def route_to(monkeypatch):
    def set_tool(name):
        monkeypatch.setattr("app.graph.router.settings.router_mode", "llm")
        monkeypatch.setattr("app.graph.router.llm_classify", lambda message: name)

    return set_tool


@pytest.mark.parametrize("message", ["Hi", "Tell me a joke", "Delete all interactions"])
def test_unsupported_messages_write_nothing(route_to, count_rows, message, db_session):
    route_to("unsupported")
    before = count_rows(Interaction)

    response = client.post("/chat", json={"message": message})

    assert response.status_code == 200
    assert response.json()["tool_name"] == "unsupported"
    assert count_rows(Interaction) == before


@pytest.mark.parametrize("message", ["Hi", "asdfgh", "Delete my last interaction"])
def test_llm_down_writes_nothing(monkeypatch, count_rows, message, db_session):
    monkeypatch.setattr("app.graph.router.settings.router_mode", "llm")

    def unavailable(message):
        raise RuntimeError("Groq unavailable")

    monkeypatch.setattr("app.graph.router.llm_classify", unavailable)
    before = count_rows(Interaction)

    client.post("/chat", json={"message": message})

    assert count_rows(Interaction) == before


def test_log_through_chat_saves_one_row(monkeypatch, route_to, create_hcp, count_rows):
    hcp = create_hcp()
    route_to("log_interaction")
    monkeypatch.setattr(
        "app.graph.tools.log_interaction.extract_interaction",
        lambda m: InteractionExtraction(
            hcp_name=f"{hcp.first_name} {hcp.last_name}",
            interaction_date="2026-10-18", channel=InteractionChannel.IN_PERSON,
            raw_notes=m, summary="Discussed Product A.", sentiment=Sentiment.POSITIVE,
        ),
    )
    before = count_rows(Interaction)

    response = client.post("/chat", json={"message": "Met the HCP today"})

    assert response.json()["tool_output"]["success"] is True
    assert count_rows(Interaction) == before + 1


def test_malformed_request_writes_nothing(count_rows, db_session):
    before = count_rows(Interaction)

    assert client.post("/chat", json={"message": "   "}).status_code == 422
    assert count_rows(Interaction) == before
