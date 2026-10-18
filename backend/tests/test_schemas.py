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

def test_interaction_create_schema_additional_fields():
    schema = InteractionCreate(
        hcp_id="123e4567-e89b-12d3-a456-426614174000",
        interaction_date=datetime.now(),
        channel=InteractionChannel.IN_PERSON,
        raw_notes="Met with doctor and nurse.",
        summary="Discussed Product A.",
        sentiment=Sentiment.POSITIVE,
        attendees=["Nurse Kelly"],
        samples_distributed=["Product A starter pack"],
        outcomes="Agreed to trial Product A.",
        follow_up_actions="Send clinical data.",
    )

    assert schema.attendees == ["Nurse Kelly"]
    assert schema.samples_distributed == ["Product A starter pack"]
    assert schema.outcomes == "Agreed to trial Product A."
    assert schema.follow_up_actions == "Send clinical data."


def test_interaction_create_schema_additional_fields_are_optional():
    schema = InteractionCreate(
        hcp_id="123e4567-e89b-12d3-a456-426614174000",
        interaction_date=datetime.now(),
        channel=InteractionChannel.PHONE,
        raw_notes="Quick call.",
        summary="Checked in.",
        sentiment=Sentiment.NEUTRAL,
    )

    assert schema.attendees is None
    assert schema.samples_distributed is None
    assert schema.outcomes is None
    assert schema.follow_up_actions is None



def test_interaction_extraction_additional_field_defaults():
    from app.schemas.ai import InteractionExtraction

    extraction = InteractionExtraction(
        hcp_name="Alice Brown",
        interaction_date="2026-10-18",
        channel=InteractionChannel.IN_PERSON,
        raw_notes="Met Alice Brown.",
        summary="Discussed Product A.",
        sentiment=Sentiment.POSITIVE,
    )

    assert extraction.attendees == []
    assert extraction.samples_distributed == []
    assert extraction.outcomes is None
    assert extraction.follow_up_actions is None


def test_extraction_schema_describes_new_fields_for_llm():
    from app.schemas.ai import InteractionExtraction

    properties = InteractionExtraction.model_json_schema()["properties"]

    for name in ("attendees", "samples_distributed", "outcomes", "follow_up_actions"):
        assert properties[name]["description"]
