"""
Reply for requests that no CRM tool handles.

Greetings, capability questions and actions that are not
supported (such as deleting interactions) end here instead of
being logged as a new interaction. Nothing is written to the
database.
"""

from __future__ import annotations

from app.graph.state import CRMState

CAPABILITIES_MESSAGE = (
    "I can help you with Healthcare Professional interactions:\n"
    "• Log a meeting — \"Met Dr. Smith today, discussed Product A\"\n"
    "• Edit the last interaction — \"Change the sentiment for Dr. Smith to positive\"\n"
    "• Show history — \"Show my interactions with Dr. Smith\"\n"
    "• Find HCPs — \"Find cardiologists at City Hospital\"\n"
    "• Suggest a follow-up — \"Suggest a follow-up for Dr. Smith\""
)

UNSUPPORTED_ACTION_MESSAGE = (
    "Sorry, I can't do that yet. Deleting interactions or "
    "Healthcare Professionals is not supported."
)

_DELETE_WORDS = ("delete", "erase", "discard", "drop")


def unsupported(state: CRMState) -> CRMState:
    """
    LangGraph tool for messages outside the CRM's capabilities.
    """

    message = state["message"].lower()

    if any(word in message for word in _DELETE_WORDS):
        reply = f"{UNSUPPORTED_ACTION_MESSAGE}\n\n{CAPABILITIES_MESSAGE}"
    else:
        reply = CAPABILITIES_MESSAGE

    state["tool_output"] = {
        "success": False,
        "error_type": "unsupported",
        "error": reply,
    }
    state["response"] = reply

    return state
