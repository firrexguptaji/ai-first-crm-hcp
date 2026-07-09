from app.graph.registry import get_tool


def test_log_interaction_registered():
    tool = get_tool("log_interaction")

    assert callable(tool)


def test_edit_interaction_registered():
    tool = get_tool("edit_interaction")

    assert callable(tool)


def test_search_hcp_registered():
    tool = get_tool("search_hcp")

    assert callable(tool)

def test_interaction_history_registered():
    tool = get_tool("interaction_history")

    assert callable(tool)
    
def test_suggest_followup_registered():
    tool = get_tool("suggest_followup")

    assert callable(tool)