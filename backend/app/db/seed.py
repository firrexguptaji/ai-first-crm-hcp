"""
Demo data for a fresh database (#64).

Inserts sample Healthcare Professionals when the table is empty,
so the AI workflow can be tried immediately after
`docker compose up`. Existing data is never changed.

Enabled with SEED_DEMO_DATA=true. Can also be run manually:

    python -m app.db.seed
"""

from __future__ import annotations

import logging

from app.db.session import SessionLocal
from app.models.healthcare_professional import HealthcareProfessional

logger = logging.getLogger(__name__)

DEMO_HCPS: list[dict[str, str]] = [
    {
        "first_name": "Alice",
        "last_name": "Brown",
        "specialization": "Cardiology",
        "organization": "City Hospital",
        "email": "alice.brown@cityhospital.example",
        "phone": "+91 90000 00001",
    },
    {
        "first_name": "John",
        "last_name": "Smith",
        "specialization": "Oncology",
        "organization": "Metro Cancer Centre",
        "email": "john.smith@metrocancer.example",
        "phone": "+91 90000 00002",
    },
    {
        "first_name": "Priya",
        "last_name": "Sharma",
        "specialization": "Endocrinology",
        "organization": "Sunrise Clinic",
        "email": "priya.sharma@sunriseclinic.example",
        "phone": "+91 90000 00003",
    },
    {
        "first_name": "Rahul",
        "last_name": "Mehta",
        "specialization": "Cardiology",
        "organization": "Apollo Heart Institute",
        "email": "rahul.mehta@apolloheart.example",
        "phone": "+91 90000 00004",
    },
    {
        "first_name": "Emily",
        "last_name": "Clark",
        "specialization": "Neurology",
        "organization": "City Hospital",
        "email": "emily.clark@cityhospital.example",
        "phone": "+91 90000 00005",
    },
    {
        "first_name": "David",
        "last_name": "Lee",
        "specialization": "General Practice",
        "organization": "Green Valley Medical",
        "email": "david.lee@greenvalley.example",
        "phone": "+91 90000 00006",
    },
]


def seed_demo_data() -> int:
    """
    Insert demo HCPs if no HCPs exist.

    Returns the number of HCPs inserted (0 when data already exists).
    """

    db = SessionLocal()

    try:
        if db.query(HealthcareProfessional).first() is not None:
            logger.info("Demo data skipped: database already has HCPs")
            return 0

        db.add_all(HealthcareProfessional(**hcp) for hcp in DEMO_HCPS)
        db.commit()

        logger.info("Demo data inserted: %d HCPs", len(DEMO_HCPS))
        return len(DEMO_HCPS)

    finally:
        db.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print(f"Inserted {seed_demo_data()} HCP(s).")
