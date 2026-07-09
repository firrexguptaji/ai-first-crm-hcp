from datetime import datetime

from app.models.enums import InteractionChannel, Sentiment
from app.schemas.healthcare_professional import (
    HealthcareProfessionalCreate,
)
from app.schemas.interaction import (
    InteractionCreate,
)


def test_hcp_create_schema():
    schema = HealthcareProfessionalCreate(
        first_name="John",
        last_name="Smith",
        specialization="Cardiology",
        organization="City Hospital",
        email="john@example.com",
        phone="+91 9999999999",
    )

    assert schema.first_name == "John"
    assert schema.organization == "City Hospital"


def test_interaction_create_schema():
    schema = InteractionCreate(
        hcp_id="123e4567-e89b-12d3-a456-426614174000",
        interaction_date=datetime.now(),
        channel=InteractionChannel.IN_PERSON,
        raw_notes="Met with doctor.",
        summary="Discussed Product A.",
        sentiment=Sentiment.POSITIVE,
        products_discussed=["Product A"],
        follow_up_required=True,
    )

    assert schema.channel == InteractionChannel.IN_PERSON
    assert schema.sentiment == Sentiment.POSITIVE