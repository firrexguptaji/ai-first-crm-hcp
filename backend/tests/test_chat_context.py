"""
The chat endpoint forwards the interaction shown in the form
to the graph as context (#81).
"""

import uuid

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def capture_state(monkeypatch):
    captured = {}

    def fake_invoke(state):
        captured.update(state)
        return {**state, "tool_name": "unsupported", "tool_output": {"success": False}}

    monkeypatch.setattr("app.api.chat.graph.invoke", fake_invoke)
    return captured


def test_interaction_id_is_forwarded_as_context(monkeypatch):
    captured = capture_state(monkeypatch)
    interaction_id = uuid.uuid4()

    response = client.post(
        "/chat",
        json={"message": "Add Dr. Patel as an attendee", "interaction_id": str(interaction_id)},
    )

    assert response.status_code == 200
    assert captured["context"] == {"interaction_id": str(interaction_id)}


def test_context_is_empty_without_interaction_id(monkeypatch):
    captured = capture_state(monkeypatch)

    client.post("/chat", json={"message": "Hi"})

    assert captured["context"] == {"interaction_id": None}


def test_invalid_interaction_id_is_rejected(monkeypatch):
    capture_state(monkeypatch)

    response = client.post("/chat", json={"message": "Hi", "interaction_id": "not-a-uuid"})

    assert response.status_code == 422
