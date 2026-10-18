from __future__ import annotations

import re

from app.graph.state import CRMState


def _words(*phrases: str) -> re.Pattern[str]:
    """
    Build a case-insensitive pattern that matches any phrase
    as whole words only ("call" must not match "recall",
    "met" must not match "metformin").
    """

    alternatives = "|".join(
        re.escape(phrase).replace(r"\ ", r"\s+")
        for phrase in phrases
    )

    return re.compile(rf"\b(?:{alternatives})\b", re.IGNORECASE)


# Imperative edit verbs. Past tense ("updated") is excluded on
# purpose: "I updated Dr. Smith on Product A" is a new interaction.
EDIT_VERBS = _words(
    "edit", "update", "modify", "change", "correct", "fix", "amend",
)

# An edit request must also refer to an existing record or field.
EDIT_TARGETS = _words(
    "interaction", "interactions", "meeting", "call", "visit",
    "record", "entry", "log", "last", "latest", "previous",
    "summary", "notes", "sentiment", "date", "channel",
    "products", "follow-up", "follow up", "follow-up date",
)

HISTORY = re.compile(
    r"\bhistory\b"
    r"|\b(?:previous|past|last|recent|all)\s+(?:interactions|meetings|visits|calls)\b"
    r"|\b(?:show|list|get|retrieve|view|fetch)\b.*\b(?:interactions|meetings|visits|calls)\b",
    re.IGNORECASE,
)

# Explicit requests for advice. A plain "follow up next week" inside
# a meeting note is NOT a request, so it is handled further down.
FOLLOWUP_REQUEST = _words(
    "suggest", "recommend", "recommendation", "recommendations",
    "next step", "next steps", "next action", "next best action",
    "what should i", "what do i do", "advice", "advise",
)

LOG = _words(
    "met", "meet", "meeting", "visited", "visit", "called", "call",
    "spoke", "talked", "discussed", "discussion", "saw", "presented",
    "emailed", "had a",
)

SEARCH = _words(
    "find", "search", "locate", "look up", "lookup", "list", "show",
    "who is", "doctors", "physicians", "hcps",
)

FOLLOWUP_MENTION = _words("follow up", "follow-up", "followup")


def classify(message: str) -> str:
    """
    Map a user message to a tool name.

    Rules are checked from most specific to least specific so that
    requests about existing records are not swallowed by the broad
    logging keywords (e.g. "Update my meeting with Dr. Smith").
    """

    if EDIT_VERBS.search(message) and EDIT_TARGETS.search(message):
        return "edit_interaction"

    if HISTORY.search(message):
        return "interaction_history"

    if FOLLOWUP_REQUEST.search(message):
        return "suggest_followup"

    if LOG.search(message):
        return "log_interaction"

    if SEARCH.search(message):
        return "search_hcp"

    if FOLLOWUP_MENTION.search(message):
        return "suggest_followup"

    # Default: treat free text as a new interaction note.
    return "log_interaction"


def route(state: CRMState) -> CRMState:
    """
    Determine which LangGraph tool should
    handle the user's request.
    """

    state["tool_name"] = classify(state["message"])

    return state
