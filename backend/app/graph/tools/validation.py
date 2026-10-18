"""
Shared validation for values extracted by the LLM.
"""

from __future__ import annotations

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
