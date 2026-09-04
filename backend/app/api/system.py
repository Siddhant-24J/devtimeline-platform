from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import os
import shutil

from app.database.session import get_db
from app.models.models import (
    Project, Milestone, Task, Commit, AutomationRun, ActivityLog, Execution
)

router = APIRouter(prefix="/system", tags=["System Maintenance"])

@router.post("/reset-data")
def reset_local_test_data(db: Session = Depends(get_db)):
    """Wipes all local test database records and deletes automation workspace folders before deployment."""
    # Delete database records
    db.query(Execution).delete()
    db.query(Commit).delete()
    db.query(AutomationRun).delete()
    db.query(ActivityLog).delete()
    db.query(Task).delete()
    db.query(Milestone).delete()
    db.query(Project).delete()
    db.commit()

    # Clean local automation workspace folders
    workspace_dir = os.path.abspath("automation_workspace")
    if os.path.exists(workspace_dir):
        for item in os.listdir(workspace_dir):
            item_path = os.path.join(workspace_dir, item)
            try:
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                else:
                    os.remove(item_path)
            except Exception:
                pass

    return {
        "status": "SUCCESS",
        "message": "All test database records and local working workspaces cleared successfully. System ready for production deployment!"
    }
