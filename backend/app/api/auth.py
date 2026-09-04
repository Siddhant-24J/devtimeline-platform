from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.models import User, GitHubAccount
from app.schemas.schemas import UserOut
from app.services.github_service import (
    get_github_oauth_url, 
    exchange_code_for_token, 
    get_authenticated_github_user
)

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.get("/github/login")
def github_login_redirect():
    """Redirects user to GitHub OAuth Authorization Page."""
    url = get_github_oauth_url()
    return RedirectResponse(url=url)

@router.get("/github/callback")
async def github_oauth_callback(code: str = Query(...), db: Session = Depends(get_db)):
    """Handles GitHub OAuth redirect callback."""
    token = await exchange_code_for_token(code)
    if not token:
        # Fallback redirect to frontend with error flag
        return RedirectResponse(url="http://localhost:3000/login?error=token_exchange_failed")

    gh_user = await get_authenticated_github_user(token)
    gh_id = str(gh_user.get("id", "12345"))
    username = gh_user.get("login", "demo_developer")

    # Find or create user
    user = db.query(User).filter(User.github_user_id == gh_id).first()
    if not user:
        user = User(
            username=username,
            email=gh_user.get("email"),
            github_user_id=gh_id,
            avatar_url=gh_user.get("avatar_url")
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    # Save or update GitHub account credentials
    gh_acc = db.query(GitHubAccount).filter(GitHubAccount.user_id == user.id).first()
    if not gh_acc:
        gh_acc = GitHubAccount(
            user_id=user.id,
            github_user_id=gh_id,
            username=username,
            access_token=token
        )
        db.add(gh_acc)
    else:
        gh_acc.access_token = token
    db.commit()

    # Redirect directly to frontend project creation page with token query param
    return RedirectResponse(url=f"http://localhost:3000/projects/new?token={token}&username={username}&status=success")

@router.post("/login/demo", response_model=UserOut)
def demo_login(db: Session = Depends(get_db)):
    """Creates or returns default demo user."""
    user = db.query(User).filter(User.username == "demo_developer").first()
    if not user:
        user = User(
            username="demo_developer",
            email="developer@devtimeline.io",
            github_user_id="12345678",
            avatar_url="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150"
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        gh_acc = GitHubAccount(
            user_id=user.id,
            github_user_id="12345678",
            username="demo_developer",
            access_token="demo_access_token_gho_12345"
        )
        db.add(gh_acc)
        db.commit()

    return user

@router.get("/me", response_model=UserOut)
def get_current_user(user_id: int = 1, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return demo_login(db)
    return user
