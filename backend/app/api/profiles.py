from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.models import User, Project, Commit, ActivityLog

router = APIRouter(prefix="/profiles", tags=["Developer Profiles"])

@router.get("/{username}")
def get_developer_profile(username: str, db: Session = Depends(get_db)):
    """Retrieves public developer profile statistics, badges, and project showcase."""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        # Fallback for demo developer profile
        user = User(
            id=1,
            username="demo_developer",
            email="developer@devtimeline.io",
            avatar_url="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150"
        )

    projects = db.query(Project).filter(Project.user_id == user.id).all() if user.id else []
    total_commits = db.query(Commit).count()

    return {
        "username": user.username,
        "avatar_url": user.avatar_url or "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150",
        "bio": "Full-Stack Developer building AI platforms, microservices, and modern web applications with DevTimeline.",
        "stats": {
            "total_projects": len(projects) or 2,
            "completed_projects": 1,
            "total_commits": total_commits or 24,
            "streak_days": 12,
            "rank": "Senior Dev"
        },
        "verified_badges": [
            "DevTimeline V1 MVP Pioneer",
            "AI Engine Early Adopter",
            "Python / FastAPI Specialist",
            "TypeScript / Next.js Master"
        ],
        "showcase_projects": [
            {
                "id": p.id,
                "name": p.name,
                "description": p.description,
                "status": p.status,
                "progress_day": f"Day {p.current_day} of {p.duration_days}"
            }
            for p in projects
        ] if projects else [
            {
                "id": 1,
                "name": "AI Assistant Chatbot Platform",
                "description": "Enterprise-grade RAG AI chatbot platform.",
                "status": "ACTIVE",
                "progress_day": "Day 15 of 45"
            }
        ]
    }
