from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.models import Project, ActivityLog
from app.services.git_sandbox import git_sandbox
from app.services.cicd_engine import cicd_engine

router = APIRouter(prefix="/deployments", tags=["Deployments & CI/CD"])

@router.post("/generate-ci/{project_id}")
def generate_cicd_pipeline(project_id: int, db: Session = Depends(get_db)):
    """Auto-generates Dockerfile, docker-compose.yml, and GitHub Actions CI workflow files."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    repo_path = git_sandbox.get_repo_path(project.repository_name or f"project-{project.id}")
    
    dockerfile, _ = cicd_engine.generate_dockerfile(repo_path, "Python / Next.js")
    compose_file, _ = cicd_engine.generate_docker_compose(repo_path)
    wf_file, _ = cicd_engine.generate_github_actions_workflow(repo_path)

    # Log audit event
    log = ActivityLog(
        user_id=project.user_id,
        project_id=project.id,
        event_type="CICD_PIPELINE_GENERATED",
        description=f"Generated production CI/CD pipeline ({dockerfile}, {compose_file}, {wf_file}) for '{project.name}'."
    )
    db.add(log)
    db.commit()

    return {
        "status": "SUCCESS",
        "project_name": project.name,
        "files_generated": [dockerfile, compose_file, wf_file]
    }
