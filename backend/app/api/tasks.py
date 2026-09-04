from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database.session import get_db
from app.models.models import Task, Milestone
from app.schemas.schemas import TaskOut, TaskCreate

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("/milestone/{milestone_id}", response_model=List[TaskOut])
def get_milestone_tasks(milestone_id: int, db: Session = Depends(get_db)):
    return db.query(Task).filter(Task.milestone_id == milestone_id).all()

@router.post("/", response_model=TaskOut)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    task = Task(**payload.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.patch("/{task_id}/complete", response_model=TaskOut)
def complete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.status = "COMPLETED"
    task.completed_at = datetime.utcnow()
    db.commit()
    db.refresh(task)
    return task
