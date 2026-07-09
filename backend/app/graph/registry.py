from __future__ import annotations

from app.graph.tools.log_interaction import log_interaction
from app.graph.tools.edit_interaction import edit_interaction

TOOLS = {
    "log_interaction": log_interaction,
    "edit_interaction": edit_interaction,
}


def get_tool(name: str):
    """
    Retrieve a registered tool.
    """

    if name not in TOOLS:
        raise ValueError(f"Unknown tool: {name}")

    return TOOLS[name]