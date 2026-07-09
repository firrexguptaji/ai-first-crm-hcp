from __future__ import annotations

from app.graph.state import CRMState


def route(state: CRMState) -> CRMState:
    """
    Determine which LangGraph tool should handle
    the current request.

    Currently only the Log Interaction tool exists.
    """

    state["tool_name"] = "log_interaction"

    return state