import pytest

from app.graph.tools.log_interaction import log_interaction
from app.models.enums import InteractionChannel, Sentiment
from app.schemas.ai import InteractionExtraction


def make_state(message="Met Dr. John Doe yesterday."):
    return {
        "message": message,
        "tool_name": "log_interaction",
        "tool_input": {},
        "tool_output": {},
        "response": "",
    }


def make_extraction(**overrides):
    data = {
        "hcp_name": "John Doe",
        "interaction_date": "yesterday",
        "channel": InteractionChannel.IN_PERSON,
        "raw_notes": "Met Dr. John Doe yesterday.",
        "summary": "Discussed Product A.",
        "sentiment": Sentiment.NEUTRAL,
    }
    data.update(overrides)
    return InteractionExtraction(**data)


def test_log_interaction_returns_state(monkeypatch):
    class FakeInteraction:
        id = "123"

    monkeypatch.setattr(
        "app.graph.tools.log_interaction.extract_interaction",
        lambda message: make_extraction(),
    )
    monkeypatch.setattr(
        "app.graph.tools.log_interaction.create_interaction_record",
        lambda extraction: FakeInteraction(),
    )

    result = log_interaction(make_state())

    assert result["tool_output"]["success"] is True
    assert result["tool_output"]["interaction_id"] == "123"


@pytest.mark.parametrize(
    "missing_field",
    ["hcp_name", "interaction_date", "summary"],
)
def test_log_interaction_incomplete_is_not_saved(monkeypatch, missing_field):
    def fail_if_called(extraction):
        raise AssertionError("Incomplete interaction must not be saved")

    monkeypatch.setattr(
        "app.graph.tools.log_interaction.extract_interaction",
        lambda message: make_extraction(**{missing_field: "  "}),
    )
    monkeypatch.setattr(
        "app.graph.tools.log_interaction.create_interaction_record",
        fail_if_called,
    )

    result = log_interaction(make_state("Had a chat."))

    assert result["tool_output"]["success"] is False
    assert result["tool_output"]["reason"] == "Incomplete interaction information"
    assert "couldn't identify" in result["response"]
