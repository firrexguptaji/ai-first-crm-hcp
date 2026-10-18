"""
Shared test configuration (#81, P1).

Test categories
---------------
unit (default)  No database, no network. Always run.
db              Real PostgreSQL in a separate TEST database.
                Run when TEST_DATABASE_URL is set.
live            Calls the Groq API. Run when RUN_LIVE_TESTS=1
                (also needs TEST_DATABASE_URL).

Database isolation
------------------
Every db test runs inside a transaction that is rolled back at the
end, so tests never depend on or change existing data. Application
code that opens its own sessions (tools, API) is redirected to the
same transaction.
"""

from __future__ import annotations

import importlib
import os
import uuid
from datetime import datetime

import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

# Allow TEST_DATABASE_URL / RUN_LIVE_TESTS in backend/.env
load_dotenv()

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
RUN_LIVE_TESTS = os.getenv("RUN_LIVE_TESTS") == "1"

# Modules that create sessions with `SessionLocal()`.
SESSION_MODULES = [
    "app.db.session",
    "app.api.dependencies",
    "app.db.seed",
    "app.graph.tools.log_interaction",
    "app.graph.tools.edit_interaction",
    "app.graph.tools.interaction_history",
    "app.graph.tools.search_hcp",
    "app.graph.tools.suggest_followup",
]


def pytest_configure(config):
    config.addinivalue_line("markers", "db: needs TEST_DATABASE_URL (separate test database)")
    config.addinivalue_line("markers", "live: calls the Groq API; needs RUN_LIVE_TESTS=1")


def pytest_collection_modifyitems(config, items):
    skip_db = pytest.mark.skip(reason="Set TEST_DATABASE_URL to run database tests")
    skip_live = pytest.mark.skip(reason="Set RUN_LIVE_TESTS=1 to run tests that call Groq")

    for item in items:
        if "db" in item.keywords and not TEST_DATABASE_URL:
            item.add_marker(skip_db)
        if "live" in item.keywords and not RUN_LIVE_TESTS:
            item.add_marker(skip_live)


@pytest.fixture(scope="session")
def test_engine():
    from app.config.settings import settings

    if TEST_DATABASE_URL == settings.database_url:
        pytest.exit(
            "TEST_DATABASE_URL must point to a separate test database, "
            "not the application database.",
            returncode=2,
        )

    engine = create_engine(TEST_DATABASE_URL)

    import app.models  # noqa: F401  register models
    from app.db.base import Base

    Base.metadata.create_all(engine)

    yield engine

    engine.dispose()


@pytest.fixture
def db_session(test_engine, monkeypatch) -> Session:
    """
    Session bound to a transaction that is rolled back after the test.

    Commits made by application code become savepoints inside that
    transaction, so they are visible during the test and discarded after.
    """

    connection = test_engine.connect()
    transaction = connection.begin()

    TestingSession = sessionmaker(
        bind=connection,
        autoflush=False,
        join_transaction_mode="create_savepoint",
    )

    for name in SESSION_MODULES:
        module = importlib.import_module(name)
        monkeypatch.setattr(module, "SessionLocal", TestingSession, raising=False)

    session = TestingSession()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


# ---------------- data factories ----------------

@pytest.fixture
def create_hcp(db_session):
    """
    Insert an HCP with a unique name so tests never collide with
    existing records.
    """

    from app.models.healthcare_professional import HealthcareProfessional

    def factory(**overrides):
        suffix = uuid.uuid4().hex[:8]
        data = {
            "first_name": "Test",
            "last_name": f"Hcp{suffix}",
            "specialization": "Cardiology",
            "organization": "Test Hospital",
            "email": f"test.{suffix}@example.com",
            "phone": None,
        }
        data.update(overrides)

        hcp = HealthcareProfessional(**data)
        db_session.add(hcp)
        db_session.commit()
        db_session.refresh(hcp)
        return hcp

    return factory


@pytest.fixture
def create_db_interaction(db_session):
    from app.models.enums import InteractionChannel, Sentiment
    from app.models.interaction import Interaction

    def factory(hcp, **overrides):
        data = {
            "hcp_id": hcp.id,
            "interaction_date": datetime(2026, 10, 18, 10, 30),
            "channel": InteractionChannel.IN_PERSON,
            "raw_notes": "Original notes.",
            "summary": "Original summary.",
            "sentiment": Sentiment.POSITIVE,
            "products_discussed": ["Product A"],
            "follow_up_required": False,
            "follow_up_date": None,
            "attendees": ["Nurse Kelly"],
            "samples_distributed": None,
            "outcomes": "Original outcome.",
            "follow_up_actions": None,
        }
        data.update(overrides)

        interaction = Interaction(**data)
        db_session.add(interaction)
        db_session.commit()
        db_session.refresh(interaction)
        return interaction

    return factory


@pytest.fixture
def snapshot(db_session):
    """
    Capture every column of a row, to prove a failed operation
    changed nothing.
    """

    def take(model):
        db_session.expire_all()
        fresh = db_session.get(type(model), model.id)
        return {
            column.name: getattr(fresh, column.name)
            for column in fresh.__table__.columns
        }

    return take


@pytest.fixture
def count_rows(db_session):
    from sqlalchemy import func, select

    def count(model):
        db_session.expire_all()
        return db_session.scalar(select(func.count()).select_from(model))

    return count


@pytest.fixture
def seed_alice(create_hcp):
    """
    Alice Brown for live workflow tests, created inside the test
    transaction (never in the application database).
    """

    return create_hcp(first_name="Alice", last_name="Brown")
