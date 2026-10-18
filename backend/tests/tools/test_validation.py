import pytest

from app.graph.tools.edit_interaction import edit_interaction
from app.graph.tools.interaction_history import history_response
from app.graph.tools.validation import require_hcp_name
from app.schemas.ai import InteractionUpdateExtraction


@pytest.mark.parametrize("name", [None, "", "UNKNOWN", "n/a"])
def test_require_hcp_name_rejects_missing(name):
    with pytest.raises(ValueError, match="Which Healthcare Professional"):
        require_hcp_name(name, "Show my interactions with Alice Brown")


def test_require_hcp_name_accepts_real_name():
    require_hcp_name("Alice Brown", "example")


def test_edit_without_hcp_asks_which_hcp(monkeypatch):
    """
    "Actually she was negative" does not name the HCP.
    """

    monkeypatch.setattr(
        "app.graph.tools.edit_interaction.extract_update",
        lambda message: InteractionUpdateExtraction(hcp_name="UNKNOWN"),
    )

    def must_not_be_called(extraction, message=None):
        raise AssertionError("Database lookup attempted")

    monkeypatch.setattr(
        "app.graph.tools.edit_interaction.update_interaction_record",
        must_not_be_called,
    )

    state = {
        "message": "Actually she was negative, not positive",
        "tool_name": "edit_interaction",
        "tool_input": {},
        "tool_output": {},
        "response": "",
    }

    with pytest.raises(ValueError, match="Which Healthcare Professional"):
        edit_interaction(state)


def test_history_response_includes_latest(make_interaction):
    response = history_response("Alice Brown", [make_interaction(), make_interaction()])

    assert response == (
        "Retrieved 2 interaction(s) for Alice Brown. "
        "Last interaction: 18-10-2026 (In Person) — Discussed Product A."
    )


def test_history_response_without_interactions():
    assert history_response("Alice Brown", []) == "No interactions found for Alice Brown."


def test_update_extraction_accepts_null_hcp_name():
    """
    Regression: the LLM returned "hcp_name": null for
    "Actually she was negative, not positive".
    """

    extraction = InteractionUpdateExtraction.model_validate({
        "hcp_name": None,
        "sentiment": "NEGATIVE",
    })

    assert extraction.hcp_name is None

    with pytest.raises(ValueError, match="Which Healthcare Professional"):
        require_hcp_name(extraction.hcp_name, "example")


@pytest.mark.parametrize(
    "schema_name",
    [
        "InteractionExtraction",
        "InteractionUpdateExtraction",
        "InteractionHistoryExtraction",
        "FollowUpExtraction",
    ],
)
def test_extraction_schemas_allow_missing_hcp_name(schema_name):
    from app.schemas import ai

    schema = getattr(ai, schema_name)

    assert schema.model_fields["hcp_name"].is_required() is False


from app.graph.tools.validation import hcp_name_from_message, resolve_hcp_name


@pytest.mark.parametrize(
    ("message", "expected"),
    [
        # Regression: LLM returned no HCP for this message (#74)
        ("Delete Product B from the products in my last meeting with Alice Brown", "Alice Brown"),
        ("Add Dr. Patel as an attendee to my meeting with Alice Brown", "Alice Brown"),
        ("Show interaction history for Dr. Alice Brown", "Alice Brown"),
        ("Suggest a follow-up for Smith", "Smith"),
        ("Remove Nurse Kelly from the attendees for Alice Brown", "Alice Brown"),
        ("Actually she was negative, not positive", None),
        ("Add Product A to the products", None),
    ],
)
def test_hcp_name_from_message(message, expected):
    assert hcp_name_from_message(message) == expected


def test_resolve_prefers_llm_name():
    assert resolve_hcp_name("Alice Brown", "meeting with Bob Stone") == "Alice Brown"


def test_resolve_falls_back_to_message():
    assert resolve_hcp_name(None, "my meeting with Alice Brown") == "Alice Brown"
    assert resolve_hcp_name("UNKNOWN", "my meeting with Alice Brown") == "Alice Brown"
