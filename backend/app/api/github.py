from fastapi import APIRouter, Depends, Request, Header
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.models import GitHubAccount, ActivityLog
from app.services.github_service import list_github_repositories

router = APIRouter(prefix="/github", tags=["GitHub Integration"])

@router.get("/repos")
async def list_user_github_repositories(token: str = None, user_id: int = 1, db: Session = Depends(get_db)):
    """Fetches user GitHub repositories using saved access token or token query param."""
    if not token or token.startswith("demo_"):
        gh_acc = db.query(GitHubAccount).order_by(GitHubAccount.id.desc()).first()
        if gh_acc and gh_acc.access_token and not gh_acc.access_token.startswith("demo_"):
            token = gh_acc.access_token

    if not token or token.startswith("demo_"):
        return []

    repos = await list_github_repositories(token)
    return repos

@router.get("/status")
def get_github_app_status():
    return {
        "connected": True,
        "app_name": "DevTimeline Bot",
        "permissions": ["contents:write", "pull_requests:write", "metadata:read"],
        "rate_limit_remaining": 4992
    }

@router.post("/webhook")
async def handle_github_webhook(request: Request, x_github_event: str = Header(None), db: Session = Depends(get_db)):
    """Listens for GitHub Webhook events (push, pull_request, workflow_run)."""
    payload = await request.json()
    
    event_type = x_github_event or "push"
    repo_name = payload.get("repository", {}).get("name", "unknown-repo")

    # Record activity log for webhook event
    log = ActivityLog(
        event_type=f"GITHUB_WEBHOOK_{event_type.upper()}",
        description=f"Received GitHub webhook event '{event_type}' for repository '{repo_name}'.",
        metadata_json=str(payload)[:500]
    )
    db.add(log)
    db.commit()

    return {"status": "accepted", "event": event_type}
