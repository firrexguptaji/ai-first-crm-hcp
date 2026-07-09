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