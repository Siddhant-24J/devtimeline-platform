import os
import zipfile
import pytest
from app.services.project_analyzer import codebase_decomposer
from app.models.models import Project, Milestone, Task, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_zip_codebase_decomposition(tmp_path):
    # Setup test DB session
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()

    # 1. Create a dummy ZIP file with sample codebase files
    zip_path = tmp_path / "sample_project.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr("config.py", "PROJECT_NAME = 'TestApp'")
        zf.writestr("models/user.py", "class User: pass")
        zf.writestr("services/auth.py", "def login(): pass")
        zf.writestr("api/routes.py", "def get_users(): pass")
        zf.writestr("tests/test_auth.py", "def test_login(): pass")
        zf.writestr("README.md", "# Test App Documentation")

    zip_bytes = zip_path.read_bytes()

    project = Project(
        id=999,
        name="Decomposed Sample App",
        description="Testing ZIP codebase decomposition engine",
        duration_days=5
    )
    db.add(project)
    db.commit()

    # 2. Verify decomposition logic
    res = codebase_decomposer.extract_and_decompose_zip(
        zip_file_bytes=zip_bytes,
        project=project,
        duration_days=5,
        db=db
    )

    assert res["total_files"] == 6
    assert res["duration_days"] == 5

    # Check created milestones & tasks
    milestones = db.query(Milestone).filter(Milestone.project_id == project.id).all()
    assert len(milestones) == 5

def test_system_reset_data_endpoint():
    response = client.post("/api/system/reset-data")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "SUCCESS"
    assert "cleared successfully" in data["message"]
