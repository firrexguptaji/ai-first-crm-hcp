from app.graph.tools.serializers import serialize_interaction
from app.models.enums import InteractionChannel, Sentiment


def test_serialize_interaction_returns_json_safe_fields(make_interaction):
    data = serialize_interaction(make_interaction())

    assert data == {
        "id": "11111111-1111-1111-1111-111111111111",
        "hcp_id": "22222222-2222-2222-2222-222222222222",
        "interaction_date": "2026-10-18T10:30:00",
        "channel": "IN_PERSON",
        "raw_notes": "Met Alice Brown at her clinic.",
        "summary": "Discussed Product A.",
        "sentiment": "POSITIVE",
        "products_discussed": ["Product A"],
        "follow_up_required": True,
        "follow_up_date": "2026-10-25",
    }


def test_serialize_interaction_handles_empty_optionals(make_interaction):
    data = serialize_interaction(
        make_interaction(
            channel=InteractionChannel.PHONE,
            sentiment=Sentiment.NEUTRAL,
            products_discussed=None,
            follow_up_required=False,
            follow_up_date=None,
        )
    )

    assert data["products_discussed"] == []
    assert data["follow_up_date"] is None
    assert data["channel"] == "PHONE"
