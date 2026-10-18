"""
Shared validation for values extracted by the LLM.
"""

from __future__ import annotations

import re

# Placeholders an LLM may return instead of leaving a field empty.
PLACEHOLDER_VALUES = {
    "unknown", "n/a", "na", "none", "null", "not specified",
    "not mentioned", "not provided", "unspecified", "-",
}


def is_missing(value: str | None) -> bool:
    """
    True when a required field is empty or only a placeholder.
    """

    if value is None:
        return True

    cleaned = value.strip().strip(".").lower()

    return not cleaned or cleaned in PLACEHOLDER_VALUES


def require_hcp_name(name: str | None, example: str) -> None:
    """
    Raise a user-facing error when the message does not name an HCP.

    The assistant has no conversation memory yet, so every request
    must name the Healthcare Professional.
    """

    if is_missing(name):
        raise ValueError(
            "Which Healthcare Professional do you mean? "
            f"Please include their name, e.g. \"{example}\"."
        )


def mentions(message: str, words: tuple[str, ...]) -> bool:
    """
    True when the message contains any of the words or phrases
    (whole words, case-insensitive).
    """

    pattern = "|".join(
        re.escape(word).replace(r"\ ", r"\s+") for word in words
    )

    return re.search(rf"\b(?:{pattern})\b", message, re.IGNORECASE) is not None


# "...meeting with Dr. Alice Brown", "...history for Alice Brown",
# "...follow-up to Smith". Two capitalised words, or one.
_HCP_NAME_AFTER_PREPOSITION = re.compile(
    r"\b(?:with|for|to|of|about)\s+"
    r"(?:(?:Dr|Doctor|Prof|Mr|Mrs|Ms)\.?\s+)?"
    r"([A-Z][a-z'-]+(?:\s+[A-Z][a-z'-]+)?)"
)

# Capitalised words that are not person names.
_NOT_NAMES = {"Product", "Products", "Nurse", "My", "The", "Phase"}


def hcp_name_from_message(message: str) -> str | None:
    """
    Fallback when the LLM does not return an HCP name: take the
    capitalised name after "with / for / to / of / about".

    The last match wins, because the HCP usually ends the sentence:
    "Delete Product B from the products in my meeting with Alice Brown".
    """

    names = [
        match.group(1)
        for match in _HCP_NAME_AFTER_PREPOSITION.finditer(message)
        if match.group(1).split()[0] not in _NOT_NAMES
    ]

    return names[-1] if names else None


def resolve_hcp_name(extracted: str | None, message: str) -> str | None:
    """
    Use the LLM's HCP name, or fall back to the message itself.
    """

    if not is_missing(extracted):
        return extracted

    return hcp_name_from_message(message)


def clean_text(value: str | None) -> str | None:
    """
    Optional text from the LLM: empty or placeholder ("N/A") → None.
    """

    if is_missing(value):
        return None

    return value.strip()


def clean_list(values: list[str] | None) -> list[str] | None:
    """
    Optional list from the LLM: drop empty or placeholder items;
    an empty result → None.
    """

    if not values:
        return None

    cleaned = [item.strip() for item in values if not is_missing(item)]

    return cleaned or None
