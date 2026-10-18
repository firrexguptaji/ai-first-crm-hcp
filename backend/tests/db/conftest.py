import pytest


@pytest.fixture(autouse=True)
def _use_test_database(db_session):
    """
    Every test in tests/db runs inside the rolled-back test
    transaction, even if it does not request db_session itself.
    Prevents accidental use of the application database.
    """

    yield
