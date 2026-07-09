from app.graph.state import CRMState


def route(state: CRMState) -> CRMState:
    """
    Determine which LangGraph tool should
    handle the user's request.
    """

    message = state["message"].lower()

    history_keywords = (
        "history",
        "interaction history",
        "previous",
        "past",
        "previous interactions",
        "last interactions",
        "retrieve interactions",
    )

    search_keywords = (
        "find",
        "search",
        "list",
        "locate",
    )

    edit_keywords = (
        "edit",
        "update",
        "modify",
        "change",
        "correct",
    )

    if any(keyword in message for keyword in history_keywords):
        state["tool_name"] = "interaction_history"

    elif any(keyword in message for keyword in search_keywords):
        state["tool_name"] = "search_hcp"

    elif any(keyword in message for keyword in edit_keywords):
        state["tool_name"] = "edit_interaction"

    else:
        state["tool_name"] = "log_interaction"

    return state