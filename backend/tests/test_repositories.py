from app.repositories.healthcare_professional import (
    HealthcareProfessionalRepository,
)
from app.repositories.interaction import (
    InteractionRepository,
)


def test_repository_classes_exist():
    assert HealthcareProfessionalRepository is not None
    assert InteractionRepository is not None