from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database.session import get_db
from app.models.models import Project, User, ActivityLog
from app.schemas.schemas import ProjectCreate, ProjectOut
from app.services.project_analyzer import codebase_decomposer

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.get("/", response_model=List[ProjectOut])
def list_user_projects(db: Session = Depends(get_db)):
    """Lists all active projects."""
    return db.query(Project).all()

@router.post("/", response_model=ProjectOut)
def create_project(project_in: ProjectCreate, db: Session = Depends(get_db)):
    """Creates new project from template or repository."""
    user = db.query(User).first()
    user_id = user.id if user else 1

    project = Project(
        user_id=user_id,
        name=project_in.name,
        description=project_in.description,
        source_type=project_in.source_type,
        repository_name=project_in.repository_name or f"repo-{project_in.name.lower().replace(' ', '-')}",
        duration_days=project_in.duration_days,
        current_day=1,
        status="ACTIVE"
    )
    db.add(project)
    db.commit()
    db.refresh(project)

    # Activity Log
    log = ActivityLog(
        user_id=user_id,
        project_id=project.id,
        event_type="PROJECT_CREATED",
        description=f"Initialized project '{project.name}' with {project.duration_days}-day roadmap."
    )
    db.add(log)
    db.commit()

    return project

@router.post("/upload-zip", response_model=ProjectOut)
async def upload_project_zip(
    file: UploadFile = File(...),
    name: str = Form(...),
    description: Optional[str] = Form(None),
    repository_name: Optional[str] = Form(None),
    duration_days: int = Form(7),
    db: Session = Depends(get_db)
):
    """Uploads project ZIP, extracts files, decomposes into daily milestones, and sets up target repo."""
    user = db.query(User).first()
    user_id = user.id if user else 1

    if not file.filename.lower().endswith(".zip"):
        raise HTTPException(status_code=400, detail="Uploaded file must be a .zip archive")

    MAX_SIZE = 500 * 1024 * 1024

    project = Project(
        user_id=user_id,
        name=name,
        description=description or f"Decomposed ZIP codebase project ({file.filename})",
        source_type="ZIP_UPLOAD",
        repository_name=repository_name or f"repo-{name.lower().replace(' ', '-')}",
        duration_days=duration_days,
        current_day=1,
        status="INITIALIZING"
    )
    db.add(project)
    db.commit()
    db.refresh(project)

    # Prepare extraction workspace and stream ZIP to disk in 1MB chunks
    import os, shutil
    upload_root = os.path.abspath("automation_workspace/uploads")
    project_upload_dir = os.path.join(upload_root, f"project_{project.id}")
    os.makedirs(project_upload_dir, exist_ok=True)
    zip_save_path = os.path.join(project_upload_dir, "source.zip")

    size = 0
    with open(zip_save_path, "wb") as buffer:
        while chunk := await file.read(1024 * 1024):
            size += len(chunk)
            if size > MAX_SIZE:
                shutil.rmtree(project_upload_dir, ignore_errors=True)
                raise HTTPException(
                    status_code=400,
                    detail="ZIP file exceeds the 500MB size limit."
                )
            buffer.write(chunk)

    # Run automated codebase decomposition across N days from stored ZIP path
    decomp_result = codebase_decomposer.extract_and_decompose_zip_file(
        zip_save_path=zip_save_path,
        project_upload_dir=project_upload_dir,
        project=project,
        duration_days=duration_days,
        db=db
    )

    # Activity Log
    log = ActivityLog(
        user_id=user_id,
        project_id=project.id,
        event_type="ZIP_CODEBASE_DECOMPOSED",
        description=f"Uploaded ZIP codebase '{file.filename}' ({decomp_result['total_files']} files) and decomposed into {duration_days} daily git milestones."
    )
    db.add(log)
    db.commit()

    return project

@router.get("/{project_id}", response_model=ProjectOut)
def get_project_by_id(project_id: int, db: Session = Depends(get_db)):
    """Retrieves full project details including milestones and tasks."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project
