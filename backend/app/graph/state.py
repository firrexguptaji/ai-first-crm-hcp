from __future__ import annotations

from typing import Any, TypedDict


class CRMState(TypedDict):
    """
    Shared state passed between LangGraph nodes.

    Each node reads the current state, updates the fields it owns,
    and returns the updated state.
    """

    # Original user request
    message: str

    # Name of the selected tool
    tool_name: str

    # Structured input passed to the tool
    tool_input: dict[str, Any]

    # Result returned by the tool
    tool_output: dict[str, Any]

    # Final response returned to the user
    response: str