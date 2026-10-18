from __future__ import annotations

import logging
import re

from app.config.settings import settings
from app.graph.state import CRMState

logger = logging.getLogger(__name__)


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
    "add", "remove", "set", "replace", "include",
)

# An edit request must also refer to an existing record or field.
EDIT_TARGETS = _words(
    "interaction", "interactions", "meeting", "call", "visit",
    "record", "entry", "log", "last", "latest", "previous",
    "summary", "notes", "sentiment", "date", "channel",
    "products", "follow-up", "follow up", "follow-up date",
    "attendee", "attendees", "sample", "samples", "outcome", "outcomes",
    "action", "actions", "follow-up actions",
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
    Keyword router: map a user message to a tool name.

    Used as the fallback when the LLM router is unavailable,
    and when ROUTER_MODE=keyword.

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


ROUTER_PROMPT = """
You route messages for a pharmaceutical CRM assistant used by
medical representatives. Choose exactly one tool.

Tools:
- log_interaction: the user describes a NEW meeting, call, visit or
  email with a Healthcare Professional (HCP).
  e.g. "Met Dr. Smith today, discussed Product A"
  e.g. "Dr. Smith rang me about side effects"
- edit_interaction: the user corrects or changes an interaction that
  was already recorded, including adding or removing attendees,
  samples or products, or changing sentiment, date, channel,
  outcomes or follow-up details.
  e.g. "Actually she was negative, not positive"
  e.g. "The meeting with Alice Brown was a phone call"
  e.g. "Add Dr. Patel as an attendee to my meeting with Alice Brown"
  e.g. "Mark follow-up as not required for Alice Brown"
- interaction_history: the user asks about PAST interactions.
  e.g. "When did I last meet Alice Brown?"
  e.g. "What did I discuss with Dr. Smith last time?"
- search_hcp: the user looks for HCPs or HCP details.
  e.g. "Do we have an oncologist named Smith?"
  e.g. "Find cardiologists at City Hospital"
- suggest_followup: the user asks for advice or a recommended next step.
  e.g. "What should I do next with Alice Brown?"
- unsupported: anything else — greetings, questions about the
  assistant, deleting records, or requests unrelated to HCP
  interactions.
  e.g. "Hi", "What can you do?", "Delete my last interaction"

Rules:
- A message that only mentions a follow-up inside a meeting note
  ("Met Dr. Smith, follow up next week") is log_interaction.
- If unsure between log_interaction and edit_interaction, choose
  edit_interaction only when the message refers to an existing
  record ("my last meeting", "actually", "change", "correct").

Message:
{message}
"""


def llm_classify(message: str) -> str:
    """
    LLM router: ask the LLM which tool should handle the message.
    """

    # Imported here so keyword-only routing works without LLM setup.
    from app.llm.groq import structured
    from app.schemas.ai import IntentClassification

    result = structured(IntentClassification).invoke(
        ROUTER_PROMPT.format(message=message)
    )

    logger.info(
        "LLM routed message to %s (%s)",
        result.tool,
        result.reason,
    )

    return result.tool


def select_tool(message: str) -> str:
    """
    Select a tool using the LLM, falling back to keywords
    if the LLM call fails or routing is set to keyword mode.
    """

    if settings.router_mode == "keyword":
        return classify(message)

    try:
        return llm_classify(message)

    except Exception:
        logger.warning(
            "LLM routing failed, using keyword fallback",
            exc_info=True,
        )
        return classify(message)


def route(state: CRMState) -> CRMState:
    """
    Determine which LangGraph tool should
    handle the user's request.
    """

    state["tool_name"] = select_tool(state["message"])

    return state
