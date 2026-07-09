from app.graph.tools.edit_interaction import edit_interaction


def test_edit_interaction_returns_state(monkeypatch):
    class FakeExtraction:
        hcp_name = "Alice Brown"

        def model_dump(self):
            return {
                "hcp_name": "Alice Brown",
                "summary": "Updated summary",
                "sentiment": "NEUTRAL",
            }

    class FakeInteraction:
        id = "123"

    def fake_extract(message):
        return FakeExtraction()

    def fake_update(extraction):
        return FakeInteraction()

    monkeypatch.setattr(
        "app.graph.tools.edit_interaction.extract_update",
        fake_extract,
    )

    monkeypatch.setattr(
        "app.graph.tools.edit_interaction.update_interaction_record",
        fake_update,
    )

    state = {
        "message": (
            "Update Dr. Alice Brown's last interaction. "
            "Change the summary and sentiment."
        ),
        "tool_name": "edit_interaction",
        "tool_input": {},
        "tool_output": {},
        "response": "",
    }

    result = edit_interaction(state)

    assert result["tool_output"]["success"] is True
    assert result["tool_output"]["interaction_id"] == "123"
    assert result["tool_input"]["hcp_name"] == "Alice Brown"
    assert result["response"] == (
        "Interaction updated successfully for Alice Brown."
    )