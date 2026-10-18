from __future__ import annotations

import logging

from langgraph.graph import END, START, StateGraph

from app.graph.registry import get_tool
from app.graph.router import route
from app.graph.state import CRMState

logger = logging.getLogger(__name__)

GENERIC_ERROR_MESSAGE = (
    "Sorry, something went wrong while processing your request. "
    "Please try again."
)


def _fail(state: CRMState, message: str, error_type: str) -> CRMState:
    """
    Record a failed tool run in the state so the user gets
    a chat reply instead of a server error.
    """

    state["tool_output"] = {
        "success": False,
        "error_type": error_type,
        "error": message,
    }
    state["response"] = message

    return state


def execute_tool(state: CRMState) -> CRMState:
    """
    Execute the selected LangGraph tool.

    Expected business errors (ValueError, e.g. "HCP not found")
    are shown to the user as-is. Unexpected errors (LLM outage,
    database failure) are logged and replaced with a generic
    message so internal details are not exposed.
    """

    tool = get_tool(state["tool_name"])

    try:
        return tool(state)

    except ValueError as error:
        return _fail(state, str(error), "validation")

    except Exception:
        logger.exception(
            "Tool '%s' failed for message: %s",
            state["tool_name"],
            state["message"],
        )
        return _fail(state, GENERIC_ERROR_MESSAGE, "internal")


builder = StateGraph(CRMState)

builder.add_node("router", route)

builder.add_node("tool", execute_tool)

builder.add_edge(START, "router")

builder.add_edge("router", "tool")

builder.add_edge("tool", END)

graph = builder.compile()
