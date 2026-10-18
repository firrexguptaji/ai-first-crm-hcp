"""
API surface guard (#81, ADR-005).

The API has no authentication. Every endpoint is listed in
docs/security/security.md. If this test fails, an endpoint was
added or removed: update the security review, then this list.
"""

from app.main import app

DOCUMENTED_ENDPOINTS = {
    ("GET", "/health"),
    ("POST", "/chat"),
    ("POST", "/hcps"),
    ("GET", "/hcps"),
    ("GET", "/hcps/{hcp_id}"),
    ("PUT", "/hcps/{hcp_id}"),
    ("DELETE", "/hcps/{hcp_id}"),
    ("POST", "/interactions"),
    ("GET", "/interactions"),
    ("GET", "/interactions/{interaction_id}"),
    ("PUT", "/interactions/{interaction_id}"),
    ("DELETE", "/interactions/{interaction_id}"),
}


def current_endpoints():
    """
    Endpoints as published in the OpenAPI schema, i.e. what
    any client can call.
    """

    paths = app.openapi()["paths"]

    return {
        (method.upper(), path)
        for path, operations in paths.items()
        for method in operations
    }


def test_api_surface_matches_security_review():
    assert current_endpoints() == DOCUMENTED_ENDPOINTS


def test_security_review_lists_every_endpoint():
    from pathlib import Path

    review = (
        Path(__file__).resolve().parents[2] / "docs" / "security" / "security.md"
    ).read_text(encoding="utf-8")

    for method, path in DOCUMENTED_ENDPOINTS:
        assert f"| {method} | `{path}` |" in review, f"{method} {path} missing from security.md"
