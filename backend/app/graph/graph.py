from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from app.graph.registry import get_tool
from app.graph.router import route
from app.graph.state import CRMState


def execute_tool(state: CRMState) -> CRMState:
    """
    Execute the selected LangGraph tool.
    """

    tool = get_tool(state["tool_name"])

    return tool(state)


builder = StateGraph(CRMState)

builder.add_node("router", route)

builder.add_node("tool", execute_tool)

builder.add_edge(START, "router")

builder.add_edge("router", "tool")

builder.add_edge("tool", END)

graph = builder.compile()