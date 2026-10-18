import pytest
from fastapi.testclient import TestClient

from app.main import app

pytestmark = [pytest.mark.live, pytest.mark.db, pytest.mark.usefixtures("seed_alice")]


client = TestClient(app)


def test_chat_endpoint():
    response = client.post(
        "/chat",
        json={
            "message": "Find Alice Brown",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert "response" in body
    assert "tool_name" in body
    assert "tool_output" in body

    assert body["tool_name"] == "search_hcp"
    assert body["tool_name"] == "search_hcp"
