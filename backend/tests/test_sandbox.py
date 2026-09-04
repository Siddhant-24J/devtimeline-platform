import os
import shutil
import pytest
from app.services.github_service import get_github_oauth_url
from app.services.git_sandbox import GitSandboxEngine
from app.models.models import Project, Task

def test_github_oauth_url_generator():
    url = get_github_oauth_url()
    assert "github.com/login/oauth/authorize" in url
    assert "client_id=" in url
    assert "scope=" in url

def test_git_sandbox_engine(tmp_path):
    sandbox = GitSandboxEngine(workspace_root=str(tmp_path))
    
    project = Project(
        id=99,
        name="Unit Test Sandbox Project",
        description="Testing live git sandbox execution",
        repository_name="test-sandbox-repo"
    )

    # 1. Prepare repository
    repo_path = sandbox.prepare_repository(project)
    assert os.path.exists(os.path.join(repo_path, ".git"))
    assert os.path.exists(os.path.join(repo_path, "README.md"))

    # 2. Checkout branch
    success = sandbox.checkout_branch(repo_path, "devtimeline/day-1")
    assert success is True

    # 3. Apply deliverable
    task = Task(
        title="Implement Core Math Engine",
        task_type="CODE",
        files_affected="src/math_engine.py"
    )
    rel_file = sandbox.apply_task_deliverable(repo_path, task, 1)
    assert os.path.exists(os.path.join(repo_path, rel_file))

    # 4. Validate codebase
    is_valid, msg = sandbox.validate_codebase(repo_path, rel_file)
    assert is_valid is True

    # 5. Commit changes
    sha, commit_msg = sandbox.commit_changes(repo_path, task, "devtimeline/day-1")
    assert len(sha) >= 7
    assert "code:" in commit_msg
