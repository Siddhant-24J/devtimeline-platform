from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.models.models import Milestone
from app.schemas.schemas import MilestoneOut, MilestoneCreate

router = APIRouter(prefix="/milestones", tags=["Milestones"])

@router.get("/project/{project_id}", response_model=List[MilestoneOut])
def get_project_milestones(project_id: int, db: Session = Depends(get_db)):
    return db.query(Milestone).filter(Milestone.project_id == project_id).order_by(Milestone.day_number.asc()).all()

@router.post("/", response_model=MilestoneOut)
def create_milestone(payload: MilestoneCreate, db: Session = Depends(get_db)):
    milestone = Milestone(**payload.model_dump())
    db.add(milestone)
    db.commit()
    db.refresh(milestone)
    return milestone
