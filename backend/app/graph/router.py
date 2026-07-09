from app.graph.state import CRMState


def route(state: CRMState) -> CRMState:
    """
    Route the request to the appropriate tool.
    """

    message = state["message"].lower()

    if any(
        keyword in message
        for keyword in (
            "update",
            "edit",
            "change",
            "modify",
            "correct",
        )
    ):
        state["tool_name"] = "edit_interaction"
    else:
        state["tool_name"] = "log_interaction"

    return state