from datetime import date, timedelta

import pytest

from app.graph.tools.edit_interaction import build_update, edit_interaction
from app.schemas.ai import InteractionUpdateExtraction


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


def test_build_update_parses_relative_follow_up_date():
    extraction = InteractionUpdateExtraction(
        hcp_name="Alice Brown",
        follow_up_date="tomorrow",
    )

    update = build_update(extraction)

    assert update.follow_up_date == date.today() + timedelta(days=1)


def test_build_update_only_sets_requested_fields():
    extraction = InteractionUpdateExtraction(
        hcp_name="Alice Brown",
        summary="Requested updated efficacy data.",
    )

    update = build_update(extraction)

    assert update.model_dump(exclude_none=True) == {
        "summary": "Requested updated efficacy data.",
    }


@pytest.mark.parametrize("field", ["interaction_date", "follow_up_date"])
def test_build_update_rejects_unreadable_date(field):
    extraction = InteractionUpdateExtraction(
        hcp_name="Alice Brown",
        **{field: "whenever she is free"},
    )

    with pytest.raises(ValueError, match="couldn't understand"):
        build_update(extraction)
