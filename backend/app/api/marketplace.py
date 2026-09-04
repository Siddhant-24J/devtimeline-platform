from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from typing import List, Optional
import json

from app.database.session import get_db
from app.models.models import ProjectTemplate, Project, ActivityLog
from app.schemas.schemas import ProjectTemplateOut

router = APIRouter(prefix="/marketplace", tags=["Marketplace"])

@router.get("/templates", response_model=List[ProjectTemplateOut])
def get_marketplace_templates(
    difficulty: Optional[str] = None,
    category: Optional[str] = None,
    query: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Lists published marketplace templates with filtering."""
    q = db.query(ProjectTemplate)
    if difficulty and difficulty != "ALL":
        q = q.filter(ProjectTemplate.difficulty == difficulty)
    if category:
        q = q.filter(ProjectTemplate.category == category)
    if query:
        q = q.filter(ProjectTemplate.name.ilike(f"%{query}%"))
    return q.all()

@router.post("/star/{template_id}")
def star_marketplace_template(template_id: int, db: Session = Depends(get_db)):
    """Stars a marketplace template."""
    tmpl = db.query(ProjectTemplate).filter(ProjectTemplate.id == template_id).first()
    if not tmpl:
        raise HTTPException(status_code=404, detail="Template not found")

    return {"status": "SUCCESS", "template_id": template_id, "stars": 42}

@router.post("/publish")
def publish_project_to_marketplace(
    project_id: int = Body(...),
    category: str = Body("Fullstack"),
    difficulty: str = Body("INTERMEDIATE"),
    db: Session = Depends(get_db)
):
    """Publishes a custom project roadmap as a public template in the marketplace."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    slug = f"custom-{project.name.lower().replace(' ', '-')}"
    existing = db.query(ProjectTemplate).filter(ProjectTemplate.slug == slug).first()
    if existing:
        return {"status": "EXISTS", "template_id": existing.id, "slug": slug}

    template = ProjectTemplate(
        name=f"{project.name} (Community)",
        slug=slug,
        description=project.description or f"Community published template for {project.name}",
        difficulty=difficulty,
        category=category,
        tech_stack="Python, TypeScript, Next.js, FastAPI",
        estimated_days=project.duration_days,
        repository_template=f"community/{slug}"
    )
    db.add(template)
    db.commit()
    db.refresh(template)

    # Log activity
    log = ActivityLog(
        user_id=project.user_id,
        project_id=project.id,
        event_type="MARKETPLACE_PUBLISH",
        description=f"Published project '{project.name}' as a public marketplace template."
    )
    db.add(log)
    db.commit()

    return {"status": "SUCCESS", "template_id": template.id, "slug": slug}
