from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.models.models import ActivityLog, Commit
from app.schemas.schemas import ActivityLogOut, CommitOut

router = APIRouter(prefix="/activity", tags=["Activity & Audit Trail"])

@router.get("/logs", response_model=List[ActivityLogOut])
def get_activity_logs(project_id: int = None, limit: int = 50, db: Session = Depends(get_db)):
    query = db.query(ActivityLog)
    if project_id:
        query = query.filter(ActivityLog.project_id == project_id)
    return query.order_by(ActivityLog.created_at.desc()).limit(limit).all()

@router.get("/commits", response_model=List[CommitOut])
def get_commits(project_id: int = None, limit: int = 50, db: Session = Depends(get_db)):
    query = db.query(Commit)
    if project_id:
        query = query.filter(Commit.project_id == project_id)
    return query.order_by(Commit.created_at.desc()).limit(limit).all()
