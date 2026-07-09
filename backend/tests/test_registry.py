from app.graph.registry import get_tool


def test_tool_registered():
    tool = get_tool("log_interaction")

    assert callable(tool)