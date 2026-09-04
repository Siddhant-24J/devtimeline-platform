from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional

from app.database.session import get_db
from app.models.models import Project, Task, ActivityLog
from app.services.ai_engine import ai_engine
from app.services.git_sandbox import git_sandbox

router = APIRouter(prefix="/ai", tags=["AI Development Engine"])

@router.post("/analyze/{project_id}")
def analyze_project_architecture(project_id: int, db: Session = Depends(get_db)):
    """Runs AI codebase architecture analysis and returns structural insights."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    repo_path = git_sandbox.get_repo_path(project.repository_name or f"project-{project.id}")
    analysis = ai_engine.analyze_codebase_architecture(repo_path)

    # Log audit event
    log = ActivityLog(
        user_id=project.user_id,
        project_id=project.id,
        event_type="AI_ARCHITECTURE_ANALYSIS",
        description=f"AI engine completed architecture scan for '{project.name}'. Detected {analysis['total_files']} files, {analysis['total_lines_of_code']} LOC."
    )
    db.add(log)
    db.commit()

    return analysis

@router.post("/generate-code")
def generate_ai_task_code(
    task_id: int = Body(...),
    file_target: Optional[str] = Body(None),
    db: Session = Depends(get_db)
):
    """Synthesizes AI production code deliverable for a specific task."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    rel_file, code = ai_engine.generate_code_implementation(task, "", file_target or task.files_affected)
    return {
        "task_id": task.id,
        "file_target": rel_file,
        "generated_code": code
    }

@router.post("/generate-tests")
def generate_ai_unit_tests(
    task_id: int = Body(...),
    file_target: str = Body(...),
    db: Session = Depends(get_db)
):
    """Auto-generates unit test suite for target module."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    test_file, test_code = ai_engine.generate_unit_tests(task, file_target)
    return {
        "test_file": test_file,
        "test_code": test_code
    }

@router.post("/repair")
def repair_code_failure(
    project_id: int = Body(...),
    file_target: str = Body(...),
    error_message: str = Body(...),
    db: Session = Depends(get_db)
):
    """Triggers self-healing bug diagnosis and code repair loop."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    repo_path = git_sandbox.get_repo_path(project.repository_name or f"project-{project.id}")
    success, msg, repaired_code = ai_engine.self_healing_repair_loop(repo_path, file_target, error_message)

    return {
        "success": success,
        "message": msg,
        "repaired_code_snippet": repaired_code[:500] if repaired_code else ""
    }

@router.post("/generate-docs/{project_id}")
def generate_project_docs(project_id: int, db: Session = Depends(get_db)):
    """Auto-generates README.md and technical documentation for project."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    repo_path = git_sandbox.get_repo_path(project.repository_name or f"project-{project.id}")
    docs = ai_engine.generate_project_documentation(repo_path, project.name)
    return docs
