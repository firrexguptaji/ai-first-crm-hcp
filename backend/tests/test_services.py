from app.services.healthcare_professional import (
    HealthcareProfessionalService,
)
from app.services.interaction import (
    InteractionService,
)


def test_service_classes_exist():
    assert HealthcareProfessionalService is not None
    assert InteractionService is not None