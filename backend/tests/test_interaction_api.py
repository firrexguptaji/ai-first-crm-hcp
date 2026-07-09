from datetime import datetime
from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_interaction_crud():
    # Create an HCP first
    hcp_payload = {
        "first_name": "Alice",
        "last_name": "Brown",
        "specialization": "Neurology",
        "organization": "General Hospital",
        "email": f"{uuid4()}@example.com",
        "phone": "+91 9999999999",
    }

    hcp_response = client.post("/hcps", json=hcp_payload)

    assert hcp_response.status_code == 201

    hcp_id = hcp_response.json()["id"]

    # Create interaction
    payload = {
        "hcp_id": hcp_id,
        "interaction_date": datetime.now().isoformat(),
        "channel": "IN_PERSON",
        "raw_notes": "Met doctor.",
        "summary": "Discussed Product A.",
        "sentiment": "POSITIVE",
        "products_discussed": ["Product A"],
        "follow_up_required": True,
        "follow_up_date": "2025-12-01",
    }

    response = client.post("/interactions", json=payload)

    assert response.status_code == 201

    data = response.json()

    interaction_id = data["id"]

    # Get
    response = client.get(f"/interactions/{interaction_id}")

    assert response.status_code == 200

    # List
    response = client.get("/interactions")

    assert response.status_code == 200

    # Update
    response = client.put(
        f"/interactions/{interaction_id}",
        json={
            "summary": "Updated summary"
        },
    )

    assert response.status_code == 200

    assert response.json()["summary"] == "Updated summary"

    # Delete
    response = client.delete(f"/interactions/{interaction_id}")

    assert response.status_code == 204

    # Verify deletion
    response = client.get(f"/interactions/{interaction_id}")

    assert response.status_code == 404