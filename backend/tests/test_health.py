from fastapi.testclient import TestClient


def test_api_health_endpoint(client: TestClient) -> None:
    """Verifies GET /api/health returns status 200 and data read from SQLite database."""
    response = client.get("/api/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "ok"
    assert data["version"] == "1.0.0"

    db = data["database"]
    assert db["status"] == "connected"
    assert db["mode"] == "WAL"
    # Ensure backend read a non-empty value seeded in the SQLite table
    assert db["value"] == "SQLite WAL Connected and Healthy"
    assert db["timestamp"] is not None


def test_api_v1_health_alias(client: TestClient) -> None:
    """Verifies GET /api/v1/health provides the exact same contract as /api/health."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["database"]["value"] == "SQLite WAL Connected and Healthy"
