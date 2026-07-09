from app.graph.router import route


def test_router_selects_log_interaction():
    state = {
        "message": "Met Dr. Smith yesterday.",
        "tool_name": "",
        "tool_input": {},
        "tool_output": {},
        "response": "",
    }

    state = route(state)

    assert state["tool_name"] == "log_interaction"