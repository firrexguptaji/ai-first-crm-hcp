"""
Fallback safety (#81, P0).

When the LLM router is unavailable, unrecognised, malformed or
destructive requests must never write to the database.
"""

import pytest
from fastapi.testclient import TestClient

from app.graph.graph import graph
from app.graph.router import classify, select_tool
from app.main import app

client = TestClient(app)

NO_WRITE_MESSAGES = [
    # Greetings and small talk
    "Hi",
    "hello there",
    "Thanks!",
    "Good morning",
    # Questions about the assistant or unrelated topics
    "What can you do?",
    "What's the weather today?",
    "Tell me a joke",
    "Who won the cricket match?",
    # Malformed or meaningless input
    "   ",
    "???",
    "asdfgh qwerty",
    "12345",
    # Destructive requests (not supported)
    "Delete my last interaction with Alice Brown",
    "Remove the meeting with Alice Brown",
    "Delete all interactions",
    "Erase this record",
]


def make_state(message):
    return {
        "message": message,
        "tool_name": "",
        "tool_input": {},
        "tool_output": {},
        "response": "",
    }


@pytest.fixture
def llm_down(monkeypatch):
    """
    LLM routing is enabled but every LLM call fails.
    """

    monkeypatch.setattr("app.graph.router.settings.router_mode", "llm")

    def unavailable(*args, **kwargs):
        raise RuntimeError("Groq unavailable")

    monkeypatch.setattr("app.graph.router.llm_classify", unavailable)


@pytest.fixture
def writes_forbidden(monkeypatch):
    """
    Fail the test if any tool tries to write to the database.
    """

    def forbidden(*args, **kwargs):
        raise AssertionError("Database write attempted")

    monkeypatch.setattr(
        "app.graph.tools.log_interaction.create_interaction_record",
        forbidden,
    )
    monkeypatch.setattr(
        "app.graph.tools.edit_interaction.update_interaction_record",
        forbidden,
    )


@pytest.mark.parametrize("message", NO_WRITE_MESSAGES)
def test_keyword_fallback_returns_unsupported(message):
    assert classify(message) == "unsupported"


@pytest.mark.parametrize("message", NO_WRITE_MESSAGES)
def test_llm_failure_falls_back_to_unsupported(llm_down, message):
    assert select_tool(message) == "unsupported"


@pytest.mark.parametrize("message", NO_WRITE_MESSAGES)
def test_no_database_write_when_llm_is_down(llm_down, writes_forbidden, message):
    result = graph.invoke(make_state(message))

    assert result["tool_name"] == "unsupported"
    assert result["tool_output"]["success"] is False
    assert result["tool_output"]["error_type"] == "unsupported"


def test_chat_endpoint_no_write_when_llm_is_down(llm_down, writes_forbidden):
    response = client.post("/chat", json={"message": "Hi"})

    assert response.status_code == 200
    assert response.json()["tool_name"] == "unsupported"


@pytest.mark.parametrize(
    "payload",
    [
        {},                       # missing message
        {"message": ""},          # empty
        {"message": "   "},       # whitespace only
        {"message": 123},         # wrong type
        {"message": "x" * 4001},  # too long
    ],
)
def test_chat_endpoint_rejects_malformed_requests(writes_forbidden, payload):
    response = client.post("/chat", json=payload)

    assert response.status_code == 422


def test_chat_endpoint_rejects_invalid_json(writes_forbidden):
    response = client.post(
        "/chat",
        content="not json",
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 422


@pytest.mark.parametrize(
    ("message", "expected"),
    [
        # Removing values from a record is still an edit, not a delete.
        ("Delete Product B from the products in my last meeting with Alice Brown", "edit_interaction"),
        ("Remove Nurse Kelly from the attendees for Alice Brown", "edit_interaction"),
        # Real interaction notes still log when the LLM is down.
        ("Met Dr. Smith yesterday.", "log_interaction"),
        ("Called Alice Brown about Product A", "log_interaction"),
    ],
)
def test_fallback_still_routes_clear_requests(llm_down, message, expected):
    assert select_tool(message) == expected
