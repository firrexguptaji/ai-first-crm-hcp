from app.graph.tools.suggest_followup import suggest_followup


def test_suggest_followup_returns_recommendation(monkeypatch):
    class FakeExtraction:
        hcp_name = "Alice Brown"

        def model_dump(self):
            return {
                "hcp_name": "Alice Brown",
            }

    class FakeRecommendation:
        recommendation = (
            "Schedule a follow-up meeting next week."
        )

        rationale = (
            "The physician showed interest in Product A."
        )

        def model_dump(self):
            return {
                "recommendation": self.recommendation,
                "rationale": self.rationale,
            }

    def fake_extract(message):
        return FakeExtraction()

    def fake_generate(extraction):
        return FakeRecommendation()

    monkeypatch.setattr(
        "app.graph.tools.suggest_followup.extract_followup",
        fake_extract,
    )

    monkeypatch.setattr(
        "app.graph.tools.suggest_followup.generate_followup",
        fake_generate,
    )

    state = {
        "message": (
            "What should I do next with Dr. Alice Brown?"
        ),
        "tool_name": "suggest_followup",
        "tool_input": {},
        "tool_output": {},
        "response": "",
    }

    result = suggest_followup(state)

    assert result["tool_output"]["success"] is True
    assert (
        result["tool_output"]["recommendation"]["recommendation"]
        == "Schedule a follow-up meeting next week."
    )

    assert (
        result["response"]
        == "Schedule a follow-up meeting next week."
    )