from app.db.base import Base
from app.models.healthcare_professional import HealthcareProfessional
from app.models.interaction import Interaction


def test_tables_registered():
    tables = Base.metadata.tables

    assert "healthcare_professionals" in tables
    assert "interactions" in tables


def test_relationships_exist():
    assert hasattr(HealthcareProfessional, "interactions")
    assert hasattr(Interaction, "hcp")

def test_interaction_has_additional_fields():
    from app.models.interaction import Interaction

    columns = Interaction.__table__.columns

    for name in ("attendees", "samples_distributed", "outcomes", "follow_up_actions"):
        assert name in columns
        assert columns[name].nullable is True
