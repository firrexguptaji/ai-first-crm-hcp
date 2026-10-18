import pytest

from app.graph.router import route


@pytest.fixture(autouse=True)
def keyword_routing(monkeypatch):
    """
    These tests cover the keyword router, so LLM routing is off.
    """

    monkeypatch.setattr("app.graph.router.settings.router_mode", "keyword")


def test_router_selects_log_interaction():
    state = {
        "message": "Met Dr. Smith yesterday.",
        "tool_name": "",
        "tool_input": {},
        "tool_output": {},
        "response": "",
    }

    state = route(state)

    assert state["tool_name"] == "log_interaction"
    


def test_router_selects_edit_interaction():
    state = {
        "message": "Update the last interaction for Dr. Alice Brown.",
        "tool_name": "",
        "tool_input": {},
        "tool_output": {},
        "response": "",
    }

    state = route(state)

    assert state["tool_name"] == "edit_interaction"
    
    


def test_router_selects_search_hcp():
    state = {
        "message": "Find cardiologists",
        "tool_name": "",
        "tool_input": {},
        "tool_output": {},
        "response": "",
    }

    result = route(state)

    assert result["tool_name"] == "search_hcp"
    
def test_router_selects_interaction_history():
    state = {
        "message": "Show interaction history for Dr. Alice Brown",
        "tool_name": "",
        "tool_input": {},
        "tool_output": {},
        "response": "",
    }

    result = route(state)

    assert result["tool_name"] == "interaction_history"
    
def test_router_selects_suggest_followup():
    state = {
        "message": (
            "What should I do next with Dr. Alice Brown?"
        ),
        "tool_name": "",
        "tool_input": {},
        "tool_output": {},
        "response": "",
    }

    result = route(state)

    assert result["tool_name"] == "suggest_followup"

import pytest

from app.graph.router import classify


@pytest.mark.parametrize(
    ("message", "expected"),
    [
        # Previously misrouted to log_interaction ("meeting"/"call" matched first)
        ("Update my meeting with Dr. Smith, sentiment was positive", "edit_interaction"),
        ("Change the summary of my last call with Alice Brown", "edit_interaction"),
        ("Suggest a follow-up after my call with Dr. Smith", "suggest_followup"),
        ("Show my past meetings with Dr. Smith", "interaction_history"),
        # Substring false positives
        # No keyword rule matches: the fallback must not guess a write.
        ("Dr. Smith asked about metformin dosing", "unsupported"),
        ("Find doctors who recall the trial", "search_hcp"),
        # Past tense "updated" in a note is a new interaction, not an edit
        ("Met Dr. Smith and updated him on Product A", "log_interaction"),
        # A follow-up mentioned inside a note stays a log
        ("Met Alice Brown today. Schedule a follow-up next week.", "log_interaction"),
        # Bare follow-up question
        ("Follow-up for Alice Brown?", "suggest_followup"),
        ("Search cardiologists at City Hospital", "search_hcp"),
        # Edits that add/remove values on the existing record (#72)
        ("Add Dr. Patel as an attendee to my meeting with Alice Brown", "edit_interaction"),
        ("Remove Nurse Kelly from the attendees for Alice Brown", "edit_interaction"),
        ("Set the outcome for my last visit with Alice Brown to agreed trial", "edit_interaction"),
        ("Add a sample of Product B to my last interaction with Alice Brown", "edit_interaction"),
        # "add" inside a new note without a record reference stays a log
        ("Met Alice Brown, she wants to add Product B to her formulary", "log_interaction"),
    ],
)
def test_classify(message, expected):
    assert classify(message) == expected
