from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# User Schemas
class UserBase(BaseModel):
    username: str
    email: Optional[str] = None
    avatar_url: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserOut(UserBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

# Milestone Schemas
class MilestoneBase(BaseModel):
    title: str
    description: Optional[str] = None
    day_number: int
    priority: str = "MEDIUM"

class MilestoneCreate(MilestoneBase):
    project_id: int

class MilestoneOut(MilestoneBase):
    id: int
    project_id: int
    status: str
    class Config:
        from_attributes = True

# Project Schemas
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    source_type: str = "BUILTIN_LIBRARY"
    duration_days: int = 30

class ProjectCreate(ProjectBase):
    template_id: Optional[int] = None
    repository_name: Optional[str] = None

class ProjectOut(ProjectBase):
    id: int
    user_id: int
    current_day: int
    status: str
    created_at: datetime
    milestones: List[MilestoneOut] = []
    class Config:
        from_attributes = True

# Template Schemas
class ProjectTemplateOut(BaseModel):
    id: int
    name: str
    slug: str
    description: str
    difficulty: str
    category: str
    tech_stack: str
    estimated_days: int
    repository_template: Optional[str] = None
    class Config:
        from_attributes = True

TemplateOut = ProjectTemplateOut

# Task Schemas
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    task_type: str = "CODE"
    priority: str = "MEDIUM"
    estimated_minutes: int = 30
    files_affected: Optional[str] = None

class TaskCreate(TaskBase):
    milestone_id: int

class TaskOut(TaskBase):
    id: int
    milestone_id: int
    status: str
    class Config:
        from_attributes = True

# Activity Log & Commit Schemas
class ActivityLogOut(BaseModel):
    id: int
    event_type: str
    description: str
    created_at: datetime
    class Config:
        from_attributes = True

class CommitOut(BaseModel):
    id: int
    github_commit_sha: str
    message: str
    branch: str
    created_at: datetime
    class Config:
        from_attributes = True
