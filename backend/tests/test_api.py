from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["app"] == "DevTimeline"

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_get_templates():
    response = client.get("/api/templates/")
    assert response.status_code == 200
    templates = response.json()
    assert len(templates) >= 1

def test_create_and_get_project():
    payload = {
        "name": "Test Portfolio Sprint",
        "source_type": "BUILTIN_LIBRARY",
        "template_id": 1,
        "duration_days": 14
    }
    response = client.post("/api/projects/", json=payload)
    assert response.status_code in (200, 201)
    data = response.json()
    assert data["name"] == "Test Portfolio Sprint"
    assert data["duration_days"] == 14
