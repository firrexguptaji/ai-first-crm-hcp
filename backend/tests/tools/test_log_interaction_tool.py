import pytest

from app.graph.tools.log_interaction import is_missing, log_interaction
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


def test_log_interaction_returns_state(monkeypatch, make_interaction):
    monkeypatch.setattr(
        "app.graph.tools.log_interaction.extract_interaction",
        lambda message: make_extraction(),
    )
    monkeypatch.setattr(
        "app.graph.tools.log_interaction.create_interaction_record",
        lambda extraction: make_interaction(),
    )

    result = log_interaction(make_state())
    output = result["tool_output"]

    assert output["success"] is True
    assert output["interaction_id"] == "11111111-1111-1111-1111-111111111111"
    assert output["hcp_name"] == "John Doe"
    assert output["interaction"]["summary"] == "Discussed Product A."
    assert output["interaction"]["channel"] == "IN_PERSON"


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
    assert result["tool_output"]["error_type"] == "validation"
    assert "couldn't identify" in result["response"]



@pytest.mark.parametrize(
    "value",
    [None, "", "  ", "Unknown", "unknown.", "N/A", "None", "not specified"],
)
def test_is_missing_detects_placeholders(value):
    assert is_missing(value) is True


@pytest.mark.parametrize("value", ["Alice Brown", "Product A discussed", "2026-10-18"])
def test_is_missing_accepts_real_values(value):
    assert is_missing(value) is False


def test_log_interaction_placeholder_name_is_not_saved(monkeypatch):
    def fail_if_called(extraction):
        raise AssertionError("Placeholder HCP must not be saved")

    monkeypatch.setattr(
        "app.graph.tools.log_interaction.extract_interaction",
        lambda message: make_extraction(hcp_name="Unknown"),
    )
    monkeypatch.setattr(
        "app.graph.tools.log_interaction.create_interaction_record",
        fail_if_called,
    )

    result = log_interaction(make_state("Had a chat."))

    assert result["tool_output"]["success"] is False
    assert "couldn't identify" in result["response"]



@pytest.mark.parametrize(
    ("missing_field", "label"),
    [
        ("hcp_name", "Healthcare Professional name"),
        ("interaction_date", "interaction date"),
        ("summary", "topics discussed"),
    ],
)
def test_log_interaction_reports_missing_field(monkeypatch, missing_field, label):
    monkeypatch.setattr(
        "app.graph.tools.log_interaction.extract_interaction",
        lambda message: make_extraction(**{missing_field: ""}),
    )

    result = log_interaction(make_state("Had a chat."))

    assert result["tool_output"]["missing"] == [label]
    assert f"Missing: {label}." in result["response"]
