from app.graph.tools.edit_interaction import edit_interaction
from app.graph.tools.interaction_history import interaction_history
from app.graph.tools.log_interaction import log_interaction
from app.graph.tools.search_hcp import search_hcp
from app.graph.tools.suggest_followup import suggest_followup

TOOLS = {
    "log_interaction": log_interaction,
    "edit_interaction": edit_interaction,
    "search_hcp": search_hcp,
    "interaction_history": interaction_history,
    "suggest_followup": suggest_followup,
}



def get_tool(name: str):
    """
    Retrieve a registered LangGraph tool.
    """

    if name not in TOOLS:
        raise ValueError(f"Unknown tool: {name}")

    return TOOLS[name]