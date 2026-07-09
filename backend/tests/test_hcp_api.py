from fastapi.testclient import TestClient
import uuid
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_hcp_crud():
    # Create
    

    payload = {
        "first_name": "John",
        "last_name": "Smith",
        "specialization": "Cardiology",
        "organization": "City Hospital",
        "email": f"{uuid.uuid4()}@example.com",
        "phone": "+91 9999999999",
    }

    response = client.post("/hcps", json=payload)

    assert response.status_code == 201

    data = response.json()

    assert data["first_name"] == "John"
    assert data["last_name"] == "Smith"

    hcp_id = data["id"]

    # Get by ID
    response = client.get(f"/hcps/{hcp_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == hcp_id
    assert data["organization"] == "City Hospital"

    # Get all
    response = client.get("/hcps")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert any(item["id"] == hcp_id for item in data)

    # Update
    update_payload = {
        "organization": "Apollo Hospital"
    }

    response = client.put(
        f"/hcps/{hcp_id}",
        json=update_payload,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["organization"] == "Apollo Hospital"

    # Delete
    response = client.delete(f"/hcps/{hcp_id}")

    assert response.status_code == 204

    # Verify deletion
    response = client.get(f"/hcps/{hcp_id}")

    assert response.status_code == 404