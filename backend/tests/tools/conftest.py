import uuid
from datetime import date, datetime

import pytest

from app.models.enums import InteractionChannel, Sentiment
from app.models.interaction import Interaction


@pytest.fixture
def make_interaction():
    """
    Build an in-memory Interaction (not saved) for tool tests.
    """

    def factory(**overrides):
        data = {
            "id": uuid.UUID("11111111-1111-1111-1111-111111111111"),
            "hcp_id": uuid.UUID("22222222-2222-2222-2222-222222222222"),
            "interaction_date": datetime(2026, 10, 18, 10, 30),
            "channel": InteractionChannel.IN_PERSON,
            "raw_notes": "Met Alice Brown at her clinic.",
            "summary": "Discussed Product A.",
            "sentiment": Sentiment.POSITIVE,
            "products_discussed": ["Product A"],
            "follow_up_required": True,
            "follow_up_date": date(2026, 10, 25),
        }
        data.update(overrides)
        return Interaction(**data)

    return factory
