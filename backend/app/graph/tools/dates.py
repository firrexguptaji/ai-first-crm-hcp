"""
Shared parsing for dates extracted by the LLM.

The prompts ask the LLM for ISO dates (YYYY-MM-DD) and give it
today's date, so most values arrive already resolved. These helpers
also accept common relative phrases as a fallback.
"""

from __future__ import annotations

import re
from datetime import date, datetime, timedelta

_RELATIVE_DAYS = {
    "today": 0,
    "tonight": 0,
    "now": 0,
    "yesterday": -1,
    "day before yesterday": -2,
    "tomorrow": 1,
    "day after tomorrow": 2,
    "next week": 7,
    "last week": -7,
    "in a week": 7,
    "in two weeks": 14,
    "next month": 30,
}

_IN_N_UNITS = re.compile(r"^in (\d+) (day|days|week|weeks)$")
_N_UNITS_AGO = re.compile(r"^(\d+) (day|days|week|weeks) ago$")


def _offset_days(text: str) -> int | None:
    if text in _RELATIVE_DAYS:
        return _RELATIVE_DAYS[text]

    for pattern, sign in ((_IN_N_UNITS, 1), (_N_UNITS_AGO, -1)):
        match = pattern.match(text)
        if match:
            amount = int(match.group(1))
            if match.group(2).startswith("week"):
                amount *= 7
            return sign * amount

    return None


def parse_date(value: str | None, today: date | None = None) -> date | None:
    """
    Parse an ISO date or a relative phrase into a date.

    Returns None when the value is empty or not understood.
    """

    if value is None or not value.strip():
        return None

    text = " ".join(value.strip().lower().split())
    today = today or date.today()

    offset = _offset_days(text)
    if offset is not None:
        return today + timedelta(days=offset)

    try:
        return date.fromisoformat(text[:10])
    except ValueError:
        return None


def parse_datetime(
    value: str | None,
    now: datetime | None = None,
) -> datetime | None:
    """
    Parse an ISO datetime, ISO date or relative phrase into a datetime.

    Relative phrases keep the current time of day.
    Returns None when the value is empty or not understood.
    """

    if value is None or not value.strip():
        return None

    now = now or datetime.now()

    try:
        return datetime.fromisoformat(value.strip())
    except ValueError:
        pass

    parsed = parse_date(value, today=now.date())
    if parsed is None:
        return None

    return datetime.combine(parsed, now.time())


def date_rules() -> str:
    """
    Prompt rules that make the LLM return resolved ISO dates.
    """

    return (
        f"- Today's date is {date.today().isoformat()}.\n"
        "- Return every date as an ISO date (YYYY-MM-DD), resolving "
        "relative phrases such as \"yesterday\" or \"next Friday\" "
        "against today's date."
    )
