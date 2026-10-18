from datetime import date, datetime

import pytest

from app.graph.tools.dates import date_rules, parse_date, parse_datetime

TODAY = date(2026, 10, 18)
NOW = datetime(2026, 10, 18, 14, 30)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("today", date(2026, 10, 18)),
        ("Tomorrow", date(2026, 10, 19)),
        ("  next   week ", date(2026, 10, 25)),
        ("yesterday", date(2026, 10, 17)),
        ("in 3 days", date(2026, 10, 21)),
        ("in 2 weeks", date(2026, 11, 1)),
        ("5 days ago", date(2026, 10, 13)),
        ("2026-11-02", date(2026, 11, 2)),
        ("2026-11-02T09:00:00", date(2026, 11, 2)),
    ],
)
def test_parse_date(value, expected):
    assert parse_date(value, today=TODAY) == expected


@pytest.mark.parametrize("value", [None, "", "   ", "whenever", "32/13/2026"])
def test_parse_date_unknown_returns_none(value):
    assert parse_date(value, today=TODAY) is None


def test_parse_datetime_relative_keeps_time_of_day():
    assert parse_datetime("yesterday", now=NOW) == datetime(2026, 10, 17, 14, 30)


def test_parse_datetime_iso():
    assert parse_datetime("2026-10-01T09:15:00", now=NOW) == datetime(2026, 10, 1, 9, 15)


def test_parse_datetime_unknown_returns_none():
    assert parse_datetime("sometime", now=NOW) is None


def test_date_rules_include_today():
    assert date.today().isoformat() in date_rules()
