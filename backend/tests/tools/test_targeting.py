"""
Explicit interaction targeting (#81, P0).

An edit must resolve exactly one interaction or ask for
clarification. It must never fall back to a guess.
"""

import uuid
from datetime import date, datetime
from types import SimpleNamespace

import pytest

from app.graph.tools.targeting import resolve_target_interaction
from app.models.enums import InteractionChannel

HCP = SimpleNamespace(id=uuid.UUID("22222222-2222-2222-2222-222222222222"))
OTHER_HCP_ID = uuid.UUID("99999999-9999-9999-9999-999999999999")
TODAY = date(2026, 10, 18)

ID_A = uuid.UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")
ID_B = uuid.UUID("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb")
ID_C = uuid.UUID("cccccccc-cccc-cccc-cccc-cccccccccccc")


class FakeService:
    """In-memory replacement for InteractionService."""

    def __init__(self, interactions):
        self.interactions = interactions

    def get_interaction(self, interaction_id):
        return next((i for i in self.interactions if i.id == interaction_id), None)

    def get_interaction_history(self, hcp_id, limit=None):
        own = [i for i in self.interactions if i.hcp_id == hcp_id]
        return sorted(own, key=lambda i: i.interaction_date, reverse=True)


@pytest.fixture
def three_interactions(make_interaction):
    return [
        make_interaction(id=ID_A, interaction_date=datetime(2026, 10, 18, 10, 0),
                         channel=InteractionChannel.PHONE, summary="Latest call"),
        make_interaction(id=ID_B, interaction_date=datetime(2026, 10, 15, 9, 0),
                         summary="Mid-October visit"),
        make_interaction(id=ID_C, interaction_date=datetime(2026, 10, 1, 9, 0),
                         summary="First visit"),
    ]


def resolve(interactions, message="Change the sentiment for Alice Brown to positive", **kwargs):
    return resolve_target_interaction(
        FakeService(interactions), HCP, "Alice Brown", message, today=TODAY, **kwargs
    )


# ---------------- 1. explicit ID ----------------

def test_explicit_id_wins(three_interactions):
    assert resolve(three_interactions, explicit_id=str(ID_C)).id == ID_C


def test_explicit_id_of_other_hcp_is_rejected(three_interactions, make_interaction):
    other = make_interaction(id=uuid.uuid4(), hcp_id=OTHER_HCP_ID)

    with pytest.raises(ValueError, match="couldn't find interaction"):
        resolve(three_interactions + [other], explicit_id=str(other.id))


def test_unknown_id_is_rejected(three_interactions):
    with pytest.raises(ValueError, match="couldn't find interaction"):
        resolve(three_interactions, explicit_id=str(uuid.uuid4()))


def test_invalid_id_is_rejected(three_interactions):
    with pytest.raises(ValueError, match="not a valid interaction ID"):
        resolve(three_interactions, explicit_id="abc123")


# ---------------- 2. date of the existing interaction ----------------

def test_target_date_selects_matching_interaction(three_interactions):
    assert resolve(three_interactions, target_date="2026-10-15").id == ID_B


def test_target_date_without_match_asks(three_interactions):
    with pytest.raises(ValueError, match="couldn't find an interaction .* on 10-10-2026"):
        resolve(three_interactions, target_date="2026-10-10")


def test_target_date_with_two_matches_asks(three_interactions, make_interaction):
    same_day = make_interaction(id=uuid.uuid4(), interaction_date=datetime(2026, 10, 15, 16, 0))

    with pytest.raises(ValueError, match="has 2 interactions on 15-10-2026"):
        resolve(three_interactions + [same_day], target_date="2026-10-15")


# ---------------- 3. explicit "last" reference ----------------

@pytest.mark.parametrize(
    "message",
    [
        "Change the sentiment of my last meeting with Alice Brown to positive",
        "Update the latest interaction with Alice Brown",
        "My most recent visit with Alice Brown was a phone call",
    ],
)
def test_explicit_latest_reference(three_interactions, message):
    assert resolve(three_interactions, message=message).id == ID_A


# ---------------- 4. interaction shown in the form ----------------

def test_context_interaction_is_used(three_interactions):
    assert resolve(three_interactions, context_id=str(ID_B)).id == ID_B


def test_context_of_other_hcp_is_ignored(three_interactions):
    with pytest.raises(ValueError, match="Which one should I update"):
        resolve(three_interactions, context_id=str(uuid.uuid4()))


def test_explicit_date_beats_context(three_interactions):
    assert resolve(three_interactions, target_date="2026-10-01", context_id=str(ID_B)).id == ID_C


# ---------------- 5. single interaction ----------------

def test_single_interaction_is_used(make_interaction):
    only = make_interaction(id=ID_A)

    assert resolve([only]).id == ID_A


# ---------------- ambiguous / empty ----------------

def test_ambiguous_without_reference_asks_and_lists(three_interactions):
    with pytest.raises(ValueError) as error:
        resolve(three_interactions)

    text = str(error.value)
    assert "Alice Brown has 3 interactions" in text
    assert "18-10-2026 (Phone) — Latest call" in text
    assert "Which one should I update?" in text


def test_no_interactions():
    with pytest.raises(ValueError, match="No interactions found for Alice Brown"):
        resolve([])


def test_long_history_is_truncated(make_interaction):
    many = [
        make_interaction(id=uuid.uuid4(), interaction_date=datetime(2026, 9, day, 9, 0))
        for day in range(1, 9)
    ]

    with pytest.raises(ValueError, match="and 3 more"):
        resolve(many)


# ---------------- graph level: ambiguity never writes ----------------

def test_edit_tool_asks_instead_of_writing(monkeypatch, three_interactions):
    """
    The edit tool raises a clarification before any update when
    the target is ambiguous. The graph returns it as a notice.
    """

    from app.graph.tools import edit_interaction as tool
    from app.schemas.ai import InteractionUpdateExtraction

    monkeypatch.setattr(
        tool, "extract_update",
        lambda message: InteractionUpdateExtraction(hcp_name="Alice Brown", outcomes="Agreed"),
    )

    class FakeSession:
        def close(self):
            pass

    monkeypatch.setattr(tool, "SessionLocal", lambda: FakeSession())
    monkeypatch.setattr(
        tool, "HealthcareProfessionalService",
        lambda repo: SimpleNamespace(search_hcp_by_name=lambda name: HCP),
    )

    service = FakeService(three_interactions)

    def forbidden(*args, **kwargs):
        raise AssertionError("Database write attempted")

    service.update_interaction = forbidden
    monkeypatch.setattr(tool, "InteractionService", lambda repo: service)
    monkeypatch.setattr(tool, "HealthcareProfessionalRepository", lambda db: None)
    monkeypatch.setattr(tool, "InteractionRepository", lambda db: None)

    state = {
        "message": "Set the outcome for Alice Brown to agreed",
        "tool_name": "edit_interaction",
        "tool_input": {},
        "tool_output": {},
        "response": "",
        "context": {},
    }

    with pytest.raises(ValueError, match="Which one should I update"):
        tool.edit_interaction(state)
