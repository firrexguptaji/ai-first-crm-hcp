from app.db.seed import DEMO_HCPS
from app.schemas.healthcare_professional import HealthcareProfessionalCreate


def test_demo_hcps_match_schema():
    for hcp in DEMO_HCPS:
        HealthcareProfessionalCreate(**hcp)


def test_demo_hcps_include_alice_brown():
    """The README and demo examples use Alice Brown."""

    names = {(hcp["first_name"], hcp["last_name"]) for hcp in DEMO_HCPS}

    assert ("Alice", "Brown") in names


def test_demo_hcp_emails_are_unique():
    emails = [hcp["email"] for hcp in DEMO_HCPS]

    assert len(emails) == len(set(emails))


def test_seed_is_off_by_default():
    from app.config.settings import Settings

    assert Settings.model_fields["seed_demo_data"].default is False
