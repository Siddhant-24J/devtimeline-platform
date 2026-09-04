import os
import pytest
from app.services.cicd_engine import CICDEngine
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_marketplace_templates_endpoint():
    response = client.get("/api/marketplace/templates")
    assert response.status_code == 200
    templates = response.json()
    assert isinstance(templates, list)

def test_marketplace_star():
    response = client.post("/api/marketplace/star/1")
    assert response.status_code == 200
    assert response.json()["status"] == "SUCCESS"

def test_developer_profile():
    response = client.get("/api/profiles/demo_developer")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "demo_developer"
    assert "stats" in data
    assert len(data["verified_badges"]) > 0

def test_cicd_engine(tmp_path):
    engine = CICDEngine()
    
    # Generate Dockerfile
    f_name, content = engine.generate_dockerfile(str(tmp_path), "Python")
    assert os.path.exists(tmp_path / "Dockerfile")
    assert "FROM python" in content

    # Generate docker-compose
    c_name, c_content = engine.generate_docker_compose(str(tmp_path))
    assert os.path.exists(tmp_path / "docker-compose.yml")

    # Generate GitHub Actions workflow
    wf_name, wf_content = engine.generate_github_actions_workflow(str(tmp_path))
    assert os.path.exists(tmp_path / ".github" / "workflows" / "devtimeline-ci.yml")
    assert "DevTimeline CI Pipeline" in wf_content
