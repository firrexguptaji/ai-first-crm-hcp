from app.graph.tools.interaction_history import interaction_history


def test_interaction_history_returns_results(monkeypatch, make_interaction):
    class FakeExtraction:
        hcp_name = "Alice Brown"
        limit = 2

        def model_dump(self):
            return {
                "hcp_name": "Alice Brown",
                "limit": 2,
            }

    def fake_extract(message):
        return FakeExtraction()

    def fake_history(extraction):
        return [make_interaction()]

    monkeypatch.setattr(
        "app.graph.tools.interaction_history.extract_history",
        fake_extract,
    )

    monkeypatch.setattr(
        "app.graph.tools.interaction_history.get_history_records",
        fake_history,
    )

    state = {
        "message": "Show interaction history for Dr. Alice Brown.",
        "tool_name": "interaction_history",
        "tool_input": {},
        "tool_output": {},
        "response": "",
    }

    result = interaction_history(state)

    assert result["tool_output"]["success"] is True
    assert result["tool_output"]["count"] == 1
    assert result["tool_output"]["hcp_name"] == "Alice Brown"
    assert result["tool_output"]["results"][0]["raw_notes"] == (
        "Met Alice Brown at her clinic."
    )
    assert result["tool_output"]["results"][0]["products_discussed"] == ["Product A"]
    assert result["response"].startswith(
        "Retrieved 1 interaction(s) for Alice Brown. Last interaction:"
    )