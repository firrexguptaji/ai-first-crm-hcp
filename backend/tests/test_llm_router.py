"""
LLM router: tool selection, keyword fallback and the
unsupported tool. The LLM is replaced with fakes, so these
tests never call Groq.
"""

import pytest

from app.graph.router import route, select_tool
from app.graph.tools.unsupported import (
    CAPABILITIES_MESSAGE,
    UNSUPPORTED_ACTION_MESSAGE,
    unsupported,
)


def make_state(message):
    return {
        "message": message,
        "tool_name": "",
        "tool_input": {},
        "tool_output": {},
        "response": "",
    }


@pytest.fixture
def llm_mode(monkeypatch):
    monkeypatch.setattr("app.graph.router.settings.router_mode", "llm")


def test_llm_choice_is_used(monkeypatch, llm_mode):
    monkeypatch.setattr(
        "app.graph.router.llm_classify",
        lambda message: "interaction_history",
    )

    # Keywords would route this to log_interaction ("meet").
    assert select_tool("When did I last meet Alice Brown?") == "interaction_history"


def test_falls_back_to_keywords_when_llm_fails(monkeypatch, llm_mode):
    def broken(message):
        raise RuntimeError("Groq unavailable")

    monkeypatch.setattr("app.graph.router.llm_classify", broken)

    assert select_tool("Find cardiologists") == "search_hcp"


def test_keyword_mode_never_calls_llm(monkeypatch):
    monkeypatch.setattr("app.graph.router.settings.router_mode", "keyword")

    def must_not_be_called(message):
        raise AssertionError("LLM router called in keyword mode")

    monkeypatch.setattr("app.graph.router.llm_classify", must_not_be_called)

    assert select_tool("Met Dr. Smith yesterday.") == "log_interaction"


def test_route_sets_tool_name(monkeypatch, llm_mode):
    monkeypatch.setattr(
        "app.graph.router.llm_classify",
        lambda message: "unsupported",
    )

    assert route(make_state("Hi"))["tool_name"] == "unsupported"


def test_unsupported_lists_capabilities():
    result = unsupported(make_state("What can you do?"))

    assert result["response"] == CAPABILITIES_MESSAGE
    assert result["tool_output"]["success"] is False
    assert result["tool_output"]["error_type"] == "unsupported"


def test_unsupported_explains_delete_is_not_supported():
    result = unsupported(make_state("Delete my last interaction with Alice Brown"))

    assert result["response"].startswith(UNSUPPORTED_ACTION_MESSAGE)
    assert CAPABILITIES_MESSAGE in result["response"]


def test_unsupported_message_writes_nothing(monkeypatch, llm_mode):
    """
    An unsupported message runs through the graph without
    touching the log tool or the database.
    """

    from app.graph.graph import graph

    monkeypatch.setattr(
        "app.graph.router.llm_classify",
        lambda message: "unsupported",
    )

    def must_not_be_called(*args, **kwargs):
        raise AssertionError("Database write attempted")

    monkeypatch.setattr(
        "app.graph.tools.log_interaction.create_interaction_record",
        must_not_be_called,
    )

    result = graph.invoke(make_state("Hi"))

    assert result["tool_name"] == "unsupported"
    assert result["tool_output"]["error_type"] == "unsupported"
