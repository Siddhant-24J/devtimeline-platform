from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.models.models import ProjectTemplate
from app.schemas.schemas import TemplateOut

router = APIRouter(prefix="/templates", tags=["Project Templates"])

@router.get("/", response_model=List[TemplateOut])
def get_templates(db: Session = Depends(get_db)):
    """Retrieve all available built-in project templates."""
    return db.query(ProjectTemplate).all()

@router.get("/{template_id}", response_model=TemplateOut)
def get_template(template_id: int, db: Session = Depends(get_db)):
    template = db.query(ProjectTemplate).filter(ProjectTemplate.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template
