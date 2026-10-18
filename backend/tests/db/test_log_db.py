"""
Log Interaction against a real database (#81, P1).
The LLM extraction is replaced with fixed values.
"""

import uuid
from types import SimpleNamespace
from datetime import date

import pytest

from app.graph.tools import log_interaction as tool
from app.models.enums import InteractionChannel, Sentiment
from app.models.interaction import Interaction
from app.schemas.ai import InteractionExtraction

pytestmark = pytest.mark.db


def state(message="Met the HCP today."):
    return {"message": message, "tool_name": "log_interaction",
            "tool_input": {}, "tool_output": {}, "response": "", "context": {}}


def extraction_for(hcp, **overrides):
    data = {
        "hcp_name": f"{hcp.first_name} {hcp.last_name}",
        "interaction_date": "2026-10-18",
        "channel": InteractionChannel.PHONE,
        "raw_notes": "Called about Product B.",
        "summary": "Discussed Product B dosing.",
        "sentiment": Sentiment.NEUTRAL,
        "products_discussed": ["Product B", "N/A"],
        "follow_up_required": True,
        "follow_up_date": "2026-10-25",
        "attendees": ["Nurse Joy", "none"],
        "samples_distributed": [],
        "outcomes": "Will review the data.",
        "follow_up_actions": "N/A",
    }
    data.update(overrides)
    return InteractionExtraction(**data)


def test_log_saves_every_extracted_field(monkeypatch, create_hcp, db_session):
    hcp = create_hcp()
    monkeypatch.setattr(tool, "extract_interaction", lambda m: extraction_for(hcp))

    result = tool.log_interaction(state())

    saved = db_session.get(Interaction, uuid.UUID(result["tool_output"]["interaction_id"]))

    assert saved.hcp_id == hcp.id
    assert saved.interaction_date.date() == date(2026, 10, 18)
    assert saved.channel == InteractionChannel.PHONE
    assert saved.raw_notes == "Called about Product B."
    assert saved.summary == "Discussed Product B dosing."
    assert saved.sentiment == Sentiment.NEUTRAL
    assert saved.products_discussed == ["Product B"]       # "N/A" removed
    assert saved.follow_up_required is True
    assert saved.follow_up_date == date(2026, 10, 25)
    assert saved.attendees == ["Nurse Joy"]                 # "none" removed
    assert saved.samples_distributed is None                # [] stored as null
    assert saved.outcomes == "Will review the data."
    assert saved.follow_up_actions is None                  # "N/A" stored as null


def test_log_returns_saved_record(monkeypatch, create_hcp):
    hcp = create_hcp()
    monkeypatch.setattr(tool, "extract_interaction", lambda m: extraction_for(hcp))

    output = tool.log_interaction(state())["tool_output"]

    assert output["success"] is True
    assert output["interaction"]["id"] == output["interaction_id"]
    assert output["interaction"]["hcp_id"] == str(hcp.id)


def test_unknown_hcp_writes_nothing(monkeypatch, count_rows):
    monkeypatch.setattr(
        tool, "extract_interaction",
        lambda m: extraction_for(SimpleNamespace(first_name="Nobody", last_name="Zzqx")),
    )
    before = count_rows(Interaction)

    with pytest.raises(ValueError, match="not found"):
        tool.log_interaction(state())

    assert count_rows(Interaction) == before


@pytest.mark.parametrize("missing", ["hcp_name", "summary", "interaction_date"])
def test_incomplete_interaction_writes_nothing(monkeypatch, create_hcp, count_rows, missing):
    hcp = create_hcp()
    monkeypatch.setattr(tool, "extract_interaction", lambda m: extraction_for(hcp, **{missing: ""}))
    before = count_rows(Interaction)

    result = tool.log_interaction(state())

    assert result["tool_output"]["success"] is False
    assert count_rows(Interaction) == before
