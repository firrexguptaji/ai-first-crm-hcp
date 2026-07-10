from app.graph.state import CRMState


def route(state: CRMState) -> CRMState:
    """
    Determine which LangGraph tool should
    handle the user's request.
    """

    message = state["message"].lower()

    # Interaction logging
    log_keywords = (
        "met",
        "meeting",
        "visited",
        "visit",
        "called",
        "call",
        "spoke",
        "talked",
        "discussed",
        "discussion",
    )

    # Interaction editing
    edit_keywords = (
        "edit",
        "update",
        "modify",
        "change",
        "correct",
    )

    # Interaction history
    history_keywords = (
        "history",
        "interaction history",
        "previous interactions",
        "retrieve interactions",
        "show interactions",
        "past interactions",
        "last interactions",
    )

    # HCP search
    search_keywords = (
        "find",
        "search",
        "locate",
        "list",
        "doctor",
        "physician",
        "hcp",
    )

    # Follow-up recommendations
    followup_keywords = (
        "follow up",
        "follow-up",
        "next step",
        "next action",
        "what should i do",
        "recommend",
        "recommendation",
        "suggest",
        "advice",
    )

    if any(keyword in message for keyword in log_keywords):
        state["tool_name"] = "log_interaction"

    elif any(keyword in message for keyword in edit_keywords):
        state["tool_name"] = "edit_interaction"

    elif any(keyword in message for keyword in history_keywords):
        state["tool_name"] = "interaction_history"

    elif any(keyword in message for keyword in search_keywords):
        state["tool_name"] = "search_hcp"

    elif any(keyword in message for keyword in followup_keywords):
        state["tool_name"] = "suggest_followup"

    else:
        # Default to logging a new interaction
        state["tool_name"] = "log_interaction"

    return state