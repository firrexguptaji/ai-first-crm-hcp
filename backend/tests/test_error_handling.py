"""
Tool and workflow errors must reach the user as chat replies,
never as HTTP 500 responses.
"""

from fastapi.testclient import TestClient

from app.graph.graph import GENERIC_ERROR_MESSAGE, graph
from app.main import app

client = TestClient(app)


def make_state(message="Met Dr. Nobody yesterday."):
    return {
        "message": message,
        "tool_name": "",
        "tool_input": {},
        "tool_output": {},
        "response": "",
    }


def raising_tool(error):
    def tool(state):
        raise error

    return lambda name: tool


def test_business_error_is_returned_to_user(monkeypatch):
    monkeypatch.setattr(
        "app.graph.graph.get_tool",
        raising_tool(ValueError("HCP 'Nobody' not found.")),
    )

    result = graph.invoke(make_state())

    assert result["tool_name"] == "log_interaction"
    assert result["tool_output"]["success"] is False
    assert result["tool_output"]["error_type"] == "validation"
    assert result["response"] == "HCP 'Nobody' not found."


def test_unexpected_error_is_hidden(monkeypatch):
    monkeypatch.setattr(
        "app.graph.graph.get_tool",
        raising_tool(RuntimeError("connection refused: db-host:5432")),
    )

    result = graph.invoke(make_state())

    assert result["tool_output"]["success"] is False
    assert result["tool_output"]["error_type"] == "internal"
    assert result["response"] == GENERIC_ERROR_MESSAGE
    assert "5432" not in result["response"]


def test_chat_endpoint_returns_200_on_tool_error(monkeypatch):
    monkeypatch.setattr(
        "app.graph.graph.get_tool",
        raising_tool(ValueError("HCP 'Nobody' not found.")),
    )

    response = client.post("/chat", json={"message": "Met Dr. Nobody yesterday."})

    assert response.status_code == 200
    body = response.json()
    assert body["tool_output"]["success"] is False
    assert body["response"] == "HCP 'Nobody' not found."


def test_chat_endpoint_returns_200_on_workflow_error(monkeypatch):
    def broken_invoke(state):
        raise RuntimeError("router exploded")

    monkeypatch.setattr("app.api.chat.graph.invoke", broken_invoke)

    response = client.post("/chat", json={"message": "anything"})

    assert response.status_code == 200
    body = response.json()
    assert body["tool_output"]["success"] is False
    assert body["response"] == GENERIC_ERROR_MESSAGE
