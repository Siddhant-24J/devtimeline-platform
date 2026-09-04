from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import json
import os
import shutil

from app.database.session import get_db
from app.models.models import (
    Project, Milestone, Task, Commit, AutomationRun, ActivityLog, Execution, GitHubAccount
)
from app.services.git_sandbox import git_sandbox
from app.services.ai_engine import ai_engine

router = APIRouter(prefix="/automation", tags=["Automation Execution Engine"])

@router.post("/trigger/{project_id}")
def trigger_daily_execution(project_id: int, db: Session = Depends(get_db)):
    """Executes daily development milestone tasks via AI Engine & Physical GitSandboxEngine."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Find active or next pending milestone
    current_milestone = (
        db.query(Milestone)
        .filter(Milestone.project_id == project.id, Milestone.status != "COMPLETED")
        .order_by(Milestone.day_number.asc())
        .first()
    )

    if not current_milestone:
        return {"status": "SUCCESS", "message": "All project milestones are already completed!"}

    # 1. Initialize local Git Repository Workspace & Branch
    repo_path = git_sandbox.prepare_repository(project)
    branch_name = f"devtimeline/day-{current_milestone.day_number}"
    git_sandbox.checkout_branch(repo_path, branch_name)

    current_milestone.status = "IN_PROGRESS"
    pending_tasks = db.query(Task).filter(Task.milestone_id == current_milestone.id, Task.status != "COMPLETED").all()

    tasks_completed = 0
    commits_created = []

    # Check if project source comes from uploaded ZIP codebase
    project_upload_dir = os.path.abspath(f"automation_workspace/uploads/project_{project.id}")
    is_zip_project = os.path.exists(project_upload_dir)

    for task in pending_tasks:
        execution = Execution(
            task_id=task.id,
            status="RUNNING",
            started_at=datetime.utcnow()
        )
        db.add(execution)
        db.commit()

        rel_file = task.files_affected or f"src/day_{current_milestone.day_number}_task_{task.id}.py"
        full_file_path = os.path.join(repo_path, rel_file)
        os.makedirs(os.path.dirname(full_file_path), exist_ok=True)

        if is_zip_project and os.path.exists(os.path.join(project_upload_dir, rel_file)):
            # Copy real decomposed source file from ZIP upload
            src_file_path = os.path.join(project_upload_dir, rel_file)
            shutil.copy2(src_file_path, full_file_path)
            val_msg = f"Copied decomposed source deliverable: {rel_file}"
            is_valid = True
        else:
            # AI Code Implementation Synthesis fallback
            _, code_content = ai_engine.generate_code_implementation(
                task=task,
                repo_path=repo_path,
                file_target=rel_file
            )
            with open(full_file_path, "w", encoding="utf-8") as f:
                f.write(code_content)

            # Codebase Validation Check
            is_valid, val_msg = git_sandbox.validate_codebase(repo_path, rel_file)

            # Self-Healing Repair Loop if Validation Fails
            if not is_valid:
                repaired_ok, repair_msg, _ = ai_engine.self_healing_repair_loop(repo_path, rel_file, val_msg)
                if repaired_ok:
                    is_valid = True
                    val_msg = f"Validated after AI self-healing repair: {repair_msg}"

        if is_valid:
            # 2. Physical Git Commit
            sha, commit_msg = git_sandbox.commit_changes(repo_path, task, branch_name)
            
            task.status = "COMPLETED"
            task.completed_at = datetime.utcnow()
            task.actual_minutes = task.estimated_minutes

            execution.status = "SUCCESS"
            execution.completed_at = datetime.utcnow()
            execution.output = f"Deliverable applied. Live Git commit [{sha}] on branch '{branch_name}'. Validation: {val_msg}"

            commit = Commit(
                project_id=project.id,
                task_id=task.id,
                github_commit_sha=sha,
                message=commit_msg,
                branch=branch_name
            )
            db.add(commit)
            commits_created.append(sha)
            tasks_completed += 1
        else:
            execution.status = "FAILED"
            execution.error_message = val_msg
            task.status = "FAILED"

    # Attempt Remote Git Push if user GitHub access token exists
    gh_acc = db.query(GitHubAccount).filter(GitHubAccount.user_id == project.user_id).first()
    pushed_remote = False
    if gh_acc and gh_acc.access_token and not gh_acc.access_token.startswith("demo_"):
        remote_url = f"https://x-access-token:{gh_acc.access_token}@github.com/{gh_acc.username}/{project.repository_name}.git"
        pushed_remote = git_sandbox.push_remote(repo_path, branch_name, remote_url)

    # Auto-generate Documentation README after milestone
    ai_engine.generate_project_documentation(repo_path, project.name)

    # Complete Milestone if all tasks finished
    remaining = db.query(Task).filter(Task.milestone_id == current_milestone.id, Task.status != "COMPLETED").count()
    if remaining == 0:
        current_milestone.status = "COMPLETED"
        current_milestone.completion_date = datetime.utcnow()
        project.current_day = min(project.duration_days, project.current_day + 1)

    # Record Automation Run
    run = AutomationRun(
        project_id=project.id,
        status="SUCCESS" if tasks_completed > 0 else "FAILED",
        tasks_attempted=len(pending_tasks),
        tasks_completed=tasks_completed,
        commits_created=len(commits_created),
        started_at=datetime.utcnow(),
        finished_at=datetime.utcnow()
    )
    db.add(run)

    # Activity Audit Log
    log = ActivityLog(
        user_id=project.user_id,
        project_id=project.id,
        event_type="DAILY_MILESTONE_EXECUTION",
        description=f"Executed daily milestone '{current_milestone.title}'. Pushed {tasks_completed} commit(s) on branch '{branch_name}'. Remote Push: {pushed_remote}.",
        metadata_json=json.dumps({"branch": branch_name, "commits": commits_created, "pushed_remote": pushed_remote})
    )
    db.add(log)
    db.commit()

    return {
        "status": "SUCCESS",
        "milestone": current_milestone.title,
        "branch": branch_name,
        "tasks_completed": tasks_completed,
        "commits_pushed": commits_created,
        "pushed_remote": pushed_remote,
        "current_day": project.current_day
    }
