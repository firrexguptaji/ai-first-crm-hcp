"""
Edit Interaction against a real database (#81, P1).

Every failed edit must leave the database unchanged; every
successful edit must change only the requested fields.
"""

from datetime import datetime

import pytest

from app.graph.tools import edit_interaction as tool
from app.models.enums import InteractionChannel, Sentiment
from app.schemas.ai import InteractionUpdateExtraction

pytestmark = pytest.mark.db

IGNORED = {"updated_at"}


def name_of(hcp):
    return f"{hcp.first_name} {hcp.last_name}"


def run_edit(monkeypatch, hcp, message, context_id=None, **fields):
    monkeypatch.setattr(
        tool, "extract_update",
        lambda m: InteractionUpdateExtraction(hcp_name=name_of(hcp), **fields),
    )
    return tool.edit_interaction({
        "message": message, "tool_name": "edit_interaction", "tool_input": {},
        "tool_output": {}, "response": "",
        "context": {"interaction_id": str(context_id) if context_id else None},
    })


def changed(before, after):
    return {k for k in before if k not in IGNORED and before[k] != after[k]}


# ---------------- partial updates ----------------

def test_only_requested_field_changes(monkeypatch, create_hcp, create_db_interaction, snapshot):
    hcp = create_hcp()
    interaction = create_db_interaction(hcp)
    before = snapshot(interaction)

    run_edit(monkeypatch, hcp, f"Set the outcome for {name_of(hcp)} to agreed to trial",
             outcomes="Agreed to trial.",
             # LLM defaults that must be ignored (not mentioned):
             sentiment=Sentiment.NEUTRAL, channel=InteractionChannel.EMAIL,
             follow_up_required=False)

    after = snapshot(interaction)
    assert changed(before, after) == {"outcomes"}
    assert after["outcomes"] == "Agreed to trial."


def test_add_and_remove_attendees_persist(monkeypatch, create_hcp, create_db_interaction, snapshot):
    hcp = create_hcp()
    interaction = create_db_interaction(hcp, attendees=["Nurse Kelly"])

    run_edit(monkeypatch, hcp, f"Add Dr. Patel as an attendee for {name_of(hcp)}",
             attendees_to_add=["Dr. Patel"])
    assert snapshot(interaction)["attendees"] == ["Nurse Kelly", "Dr. Patel"]

    run_edit(monkeypatch, hcp, f"Remove Kelly from the attendees for {name_of(hcp)}",
             attendees_to_remove=["Kelly"])
    assert snapshot(interaction)["attendees"] == ["Dr. Patel"]


def test_mentioned_sentiment_changes(monkeypatch, create_hcp, create_db_interaction, snapshot):
    hcp = create_hcp()
    interaction = create_db_interaction(hcp, sentiment=Sentiment.POSITIVE)
    before = snapshot(interaction)

    run_edit(monkeypatch, hcp, f"Actually {name_of(hcp)} was negative",
             sentiment=Sentiment.NEGATIVE)

    after = snapshot(interaction)
    assert changed(before, after) == {"sentiment"}
    assert after["sentiment"] == Sentiment.NEGATIVE


# ---------------- targeting ----------------

def test_context_interaction_is_edited_and_other_untouched(
    monkeypatch, create_hcp, create_db_interaction, snapshot,
):
    hcp = create_hcp()
    older = create_db_interaction(hcp, interaction_date=datetime(2026, 10, 1, 9))
    newer = create_db_interaction(hcp, interaction_date=datetime(2026, 10, 18, 9))
    newer_before = snapshot(newer)

    run_edit(monkeypatch, hcp, f"Set the outcome for {name_of(hcp)} to declined",
             context_id=older.id, outcomes="Declined.")

    assert snapshot(older)["outcomes"] == "Declined."
    assert snapshot(newer) == newer_before


def test_target_date_selects_interaction(monkeypatch, create_hcp, create_db_interaction, snapshot):
    hcp = create_hcp()
    first = create_db_interaction(hcp, interaction_date=datetime(2026, 10, 1, 9))
    second = create_db_interaction(hcp, interaction_date=datetime(2026, 10, 15, 9))
    second_before = snapshot(second)

    run_edit(monkeypatch, hcp, f"Set the outcome of my meeting with {name_of(hcp)} on 1 October",
             target_date="2026-10-01", outcomes="Requested samples.")

    assert snapshot(first)["outcomes"] == "Requested samples."
    assert snapshot(second) == second_before


# ---------------- failures leave the database unchanged ----------------

def test_ambiguous_target_changes_nothing(monkeypatch, create_hcp, create_db_interaction, snapshot):
    hcp = create_hcp()
    a = create_db_interaction(hcp, interaction_date=datetime(2026, 10, 1, 9))
    b = create_db_interaction(hcp, interaction_date=datetime(2026, 10, 15, 9))
    before = (snapshot(a), snapshot(b))

    with pytest.raises(ValueError, match="Which one should I update"):
        run_edit(monkeypatch, hcp, f"Set the outcome for {name_of(hcp)} to agreed",
                 outcomes="Agreed.")

    assert (snapshot(a), snapshot(b)) == before


def test_nothing_to_update_changes_nothing(monkeypatch, create_hcp, create_db_interaction, snapshot):
    hcp = create_hcp()
    interaction = create_db_interaction(hcp)
    before = snapshot(interaction)

    with pytest.raises(ValueError, match="couldn't tell what to change"):
        run_edit(monkeypatch, hcp, f"Edit the outcome for {name_of(hcp)}",
                 sentiment=Sentiment.NEUTRAL)   # default only, not mentioned

    assert snapshot(interaction) == before


def test_unreadable_date_changes_nothing(monkeypatch, create_hcp, create_db_interaction, snapshot):
    hcp = create_hcp()
    interaction = create_db_interaction(hcp)
    before = snapshot(interaction)

    with pytest.raises(ValueError, match="couldn't understand"):
        run_edit(monkeypatch, hcp, f"Set the follow-up for {name_of(hcp)} to whenever",
                 follow_up_date="whenever she is free")

    assert snapshot(interaction) == before


def test_unknown_hcp_changes_nothing(monkeypatch, create_hcp, create_db_interaction, snapshot):
    hcp = create_hcp()
    interaction = create_db_interaction(hcp)
    before = snapshot(interaction)

    monkeypatch.setattr(
        tool, "extract_update",
        lambda m: InteractionUpdateExtraction(hcp_name="Nobody Zzqx", outcomes="x"),
    )

    with pytest.raises(ValueError, match="not found"):
        tool.edit_interaction({
            "message": "Set the outcome for Nobody Zzqx", "tool_name": "edit_interaction",
            "tool_input": {}, "tool_output": {}, "response": "", "context": {},
        })

    assert snapshot(interaction) == before


def test_other_hcps_interaction_id_is_rejected(
    monkeypatch, create_hcp, create_db_interaction, snapshot,
):
    hcp = create_hcp()
    other = create_hcp()
    mine = create_db_interaction(hcp)
    theirs = create_db_interaction(other)
    before = (snapshot(mine), snapshot(theirs))

    with pytest.raises(ValueError, match="couldn't find interaction"):
        run_edit(monkeypatch, hcp, f"Set the outcome for {name_of(hcp)}",
                 interaction_id=str(theirs.id), outcomes="Hijacked.")

    assert (snapshot(mine), snapshot(theirs)) == before
