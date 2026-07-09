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
    
    
from app.graph.router import route


def test_router_selects_edit_interaction():
    state = {
        "message": "Update the last interaction for Dr. Alice Brown.",
        "tool_name": "",
        "tool_input": {},
        "tool_output": {},
        "response": "",
    }

    state = route(state)

    assert state["tool_name"] == "edit_interaction"