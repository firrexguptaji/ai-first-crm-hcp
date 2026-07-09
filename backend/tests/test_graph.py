from app.graph.graph import graph


def test_graph_invocation():
    result = graph.invoke(
        {
            "message": "Hello! Who are you?"
        }
    )

    assert "message" in result
    assert isinstance(result["message"], str)
    assert len(result["message"]) > 0

    print(result["message"])