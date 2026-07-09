from app.graph.tools.log_interaction import log_interaction


def test_log_interaction_returns_state(monkeypatch):
    def fake_extract(message):
        class FakeExtraction:
            hcp_name = "John Doe"

            def model_dump(self):
                return {"hcp_name": "John Doe"}

        return FakeExtraction()

    def fake_create(extraction):
        class FakeInteraction:
            id = "123"

        return FakeInteraction()

    monkeypatch.setattr(
        "app.graph.tools.log_interaction.extract_interaction",
        fake_extract,
    )

    monkeypatch.setattr(
        "app.graph.tools.log_interaction.create_interaction_record",
        fake_create,
    )

    state = {
        "message": "Met Dr. John Doe yesterday.",
        "tool_name": "log_interaction",
        "tool_input": {},
        "tool_output": {},
        "response": "",
    }

    result = log_interaction(state)

    assert result["tool_output"]["success"] is True