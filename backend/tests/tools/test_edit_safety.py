"""
Edit safety (#74): edits change only what the user asked for.
"""

import pytest

from app.graph.tools.edit_interaction import (
    NOTHING_TO_UPDATE_MESSAGE,
    build_update,
    merge_list,
)
from app.graph.tools.validation import mentions
from app.models.enums import InteractionChannel, Sentiment
from app.schemas.ai import InteractionUpdateExtraction


def extraction(**fields):
    return InteractionUpdateExtraction(hcp_name="Alice Brown", **fields)


def changes(update):
    return update.model_dump(exclude_none=True)


# ---------------- defaults are ignored unless mentioned ----------------

def test_llm_default_sentiment_ignored_when_not_mentioned(make_interaction):
    update = build_update(
        extraction(sentiment=Sentiment.NEUTRAL, attendees_to_add=["Dr. Patel"]),
        "Add Dr. Patel as an attendee to my meeting with Alice Brown",
        make_interaction(),
    )

    assert "sentiment" not in changes(update)


def test_sentiment_applied_when_mentioned(make_interaction):
    update = build_update(
        extraction(sentiment=Sentiment.NEGATIVE),
        "Actually she was negative, not positive",
        make_interaction(),
    )

    assert changes(update) == {"sentiment": Sentiment.NEGATIVE}


def test_llm_default_channel_ignored_when_not_mentioned(make_interaction):
    update = build_update(
        extraction(channel=InteractionChannel.IN_PERSON, outcomes="Agreed to trial."),
        "Set the outcome for Alice Brown to agreed to trial",
        make_interaction(),
    )

    assert "channel" not in changes(update)


def test_channel_applied_when_mentioned(make_interaction):
    update = build_update(
        extraction(channel=InteractionChannel.PHONE),
        "The meeting with Alice Brown was actually a phone call",
        make_interaction(),
    )

    assert changes(update) == {"channel": InteractionChannel.PHONE}


def test_llm_default_follow_up_flag_ignored_when_not_mentioned(make_interaction):
    update = build_update(
        extraction(follow_up_required=False, outcomes="Agreed to trial."),
        "Set the outcome for Alice Brown to agreed to trial",
        make_interaction(),
    )

    assert "follow_up_required" not in changes(update)


def test_follow_up_flag_applied_when_mentioned(make_interaction):
    update = build_update(
        extraction(follow_up_required=False),
        "Mark follow-up as not required for Alice Brown",
        make_interaction(),
    )

    assert changes(update) == {"follow_up_required": False}


def test_follow_up_date_implies_follow_up_required(make_interaction):
    update = build_update(
        extraction(follow_up_date="2026-10-25"),
        "Set the follow-up date for Alice Brown to 2026-10-25",
        make_interaction(follow_up_required=False),
    )

    assert changes(update)["follow_up_required"] is True


# ---------------- list add / remove ----------------

def test_add_attendee_keeps_existing(make_interaction):
    update = build_update(
        extraction(attendees_to_add=["Dr. Patel"]),
        "Add Dr. Patel as an attendee to my meeting with Alice Brown",
        make_interaction(attendees=["Nurse Kelly"]),
    )

    assert changes(update) == {"attendees": ["Nurse Kelly", "Dr. Patel"]}


def test_remove_attendee_by_partial_name(make_interaction):
    update = build_update(
        extraction(attendees_to_remove=["Kelly"]),
        "Remove Kelly from the attendees for Alice Brown",
        make_interaction(attendees=["Nurse Kelly", "Dr. Patel"]),
    )

    assert changes(update) == {"attendees": ["Dr. Patel"]}


def test_remove_product(make_interaction):
    update = build_update(
        extraction(products_to_remove=["Product A"]),
        "Delete Product A from the products in my last meeting with Alice Brown",
        make_interaction(products_discussed=["Product A", "Product B"]),
    )

    assert changes(update) == {"products_discussed": ["Product B"]}


def test_add_sample_to_empty_list(make_interaction):
    update = build_update(
        extraction(samples_to_add=["Product B sample"]),
        "Add a sample of Product B for Alice Brown",
        make_interaction(samples_distributed=None),
    )

    assert changes(update) == {"samples_distributed": ["Product B sample"]}


def test_full_replacement_list(make_interaction):
    update = build_update(
        extraction(attendees=["Dr. Patel", "Nurse Joy"]),
        "The attendees were Dr. Patel and Nurse Joy for Alice Brown",
        make_interaction(attendees=["Nurse Kelly"]),
    )

    assert changes(update) == {"attendees": ["Dr. Patel", "Nurse Joy"]}


@pytest.mark.parametrize(
    ("current", "replacement", "to_add", "to_remove", "expected"),
    [
        (["A"], None, None, None, None),            # nothing requested
        (["A"], None, ["a"], None, None),           # duplicate add, no change
        (["A"], None, None, ["Z"], None),           # removing absent item
        (None, None, ["A"], None, ["A"]),
        (["A", "B"], None, ["C"], ["A"], ["B", "C"]),
        (["A"], [], None, None, None),              # empty replacement ignored
    ],
)
def test_merge_list(current, replacement, to_add, to_remove, expected):
    assert merge_list(current, replacement, to_add, to_remove) == expected


# ---------------- nothing to update ----------------

def test_nothing_to_update_when_only_defaults(make_interaction):
    update = build_update(
        extraction(sentiment=Sentiment.NEUTRAL, follow_up_required=False),
        "Edit the outcome for Alice Brown",
        make_interaction(),
    )

    assert changes(update) == {}
    assert "couldn't tell what to change" in NOTHING_TO_UPDATE_MESSAGE


# ---------------- mentions helper ----------------

@pytest.mark.parametrize(
    ("message", "words", "expected"),
    [
        ("It was a phone call", ("phone",), True),
        ("She was in person", ("in person",), True),
        ("Recall the details", ("call",), False),
        ("She followed up later", ("follow",), False),
    ],
)
def test_mentions(message, words, expected):
    assert mentions(message, words) is expected
