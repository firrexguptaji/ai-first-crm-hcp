from app.graph.tools.interaction_history import interaction_history


def test_interaction_history_returns_results(monkeypatch):
    class FakeExtraction:
        hcp_name = "Alice Brown"
        limit = 2

        def model_dump(self):
            return {
                "hcp_name": "Alice Brown",
                "limit": 2,
            }

    class FakeInteraction:
        id = "123"
        interaction_date = __import__("datetime").datetime.now()

        class Channel:
            value = "IN_PERSON"

        class Sentiment:
            value = "POSITIVE"

        channel = Channel()
        sentiment = Sentiment()

        summary = "Discussed Product A"
        follow_up_required = True
        follow_up_date = None

    def fake_extract(message):
        return FakeExtraction()

    def fake_history(extraction):
        return [FakeInteraction()]

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
    assert result["response"] == (
        "Retrieved 1 interaction(s) for Alice Brown."
    )