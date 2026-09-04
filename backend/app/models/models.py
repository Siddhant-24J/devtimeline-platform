from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum as SQLEnum
)
from sqlalchemy.orm import relationship
import enum
from app.database.session import Base

# Enums
class ProjectStatus(str, enum.Enum):
    PLANNING = "PLANNING"
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    ARCHIVED = "ARCHIVED"

class SourceType(str, enum.Enum):
    GITHUB_REPO = "GITHUB_REPO"
    UPLOAD_ZIP = "UPLOAD_ZIP"
    BUILTIN_LIBRARY = "BUILTIN_LIBRARY"

class DifficultyLevel(str, enum.Enum):
    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"

class MilestoneStatus(str, enum.Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class TaskType(str, enum.Enum):
    CODE = "CODE"
    TEST = "TEST"
    DOCUMENTATION = "DOCUMENTATION"
    REFACTOR = "REFACTOR"
    CONFIGURATION = "CONFIGURATION"
    DATABASE = "DATABASE"
    FRONTEND = "FRONTEND"
    BACKEND = "BACKEND"
    DEVOPS = "DEVOPS"

class TaskStatus(str, enum.Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class ExecutionStatus(str, enum.Enum):
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

# Models

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    github_user_id = Column(String, unique=True, index=True, nullable=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    avatar_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    github_account = relationship("GitHubAccount", back_populates="user", uselist=False)
    projects = relationship("Project", back_populates="user")
    logs = relationship("ActivityLog", back_populates="user")


class GitHubAccount(Base):
    __tablename__ = "github_accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    github_user_id = Column(String, unique=True, index=True)
    username = Column(String)
    installation_id = Column(String, nullable=True)
    access_token = Column(String, nullable=True)
    token_expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="github_account")


class ProjectTemplate(Base):
    __tablename__ = "project_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    slug = Column(String, unique=True, index=True)
    description = Column(Text)
    difficulty = Column(String, default="BEGINNER")
    category = Column(String, default="General")
    tech_stack = Column(Text) # JSON string or comma-separated
    estimated_days = Column(Integer, default=30)
    repository_template = Column(String, nullable=True)
    features = Column(Text, nullable=True) # JSON list
    version = Column(String, default="1.0.0")
    created_at = Column(DateTime, default=datetime.utcnow)

    projects = relationship("Project", back_populates="template")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    source_type = Column(String, default="BUILTIN_LIBRARY")
    repository_name = Column(String, nullable=True)
    github_repo_url = Column(String, nullable=True)
    template_id = Column(Integer, ForeignKey("project_templates.id"), nullable=True)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)
    duration_days = Column(Integer, default=30)
    current_day = Column(Integer, default=1)
    status = Column(String, default="PLANNING")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="projects")
    template = relationship("ProjectTemplate", back_populates="projects")
    milestones = relationship("Milestone", back_populates="project", cascade="all, delete-orphan")
    commits = relationship("Commit", back_populates="project", cascade="all, delete-orphan")
    automation_runs = relationship("AutomationRun", back_populates="project", cascade="all, delete-orphan")
    logs = relationship("ActivityLog", back_populates="project", cascade="all, delete-orphan")


class Milestone(Base):
    __tablename__ = "milestones"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    title = Column(String)
    description = Column(Text, nullable=True)
    day_number = Column(Integer)
    priority = Column(String, default="MEDIUM") # LOW, MEDIUM, HIGH
    status = Column(String, default="PENDING")
    start_date = Column(DateTime, nullable=True)
    completion_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="milestones")
    tasks = relationship("Task", back_populates="milestone", cascade="all, delete-orphan")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    milestone_id = Column(Integer, ForeignKey("milestones.id"))
    title = Column(String)
    description = Column(Text, nullable=True)
    task_type = Column(String, default="CODE")
    status = Column(String, default="PENDING")
    priority = Column(String, default="MEDIUM")
    estimated_minutes = Column(Integer, default=60)
    actual_minutes = Column(Integer, nullable=True)
    files_affected = Column(Text, nullable=True) # Comma-separated or JSON
    expected_output = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    milestone = relationship("Milestone", back_populates="tasks")
    executions = relationship("Execution", back_populates="task", cascade="all, delete-orphan")
    commits = relationship("Commit", back_populates="task")
    
    # Task dependencies
    dependencies = relationship(
        "TaskDependency",
        foreign_keys="TaskDependency.task_id",
        back_populates="task",
        cascade="all, delete-orphan"
    )


class TaskDependency(Base):
    __tablename__ = "task_dependencies"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    depends_on_task_id = Column(Integer, ForeignKey("tasks.id"))

    task = relationship("Task", foreign_keys=[task_id], back_populates="dependencies")


class Execution(Base):
    __tablename__ = "executions"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    status = Column(String, default="RUNNING")
    output = Column(Text, nullable=True)
    error_message = Column(Text, nullable=True)

    task = relationship("Task", back_populates="executions")


class Commit(Base):
    __tablename__ = "commits"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    github_commit_sha = Column(String, nullable=True)
    message = Column(String)
    branch = Column(String, default="main")
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="commits")
    task = relationship("Task", back_populates="commits")


class AutomationRun(Base):
    __tablename__ = "automation_runs"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    run_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="RUNNING")
    tasks_attempted = Column(Integer, default=0)
    tasks_completed = Column(Integer, default=0)
    commits_created = Column(Integer, default=0)
    error = Column(Text, nullable=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    finished_at = Column(DateTime, nullable=True)

    project = relationship("Project", back_populates="automation_runs")


class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    event_type = Column(String, index=True) # e.g. PROJECT_CREATED, TASK_COMPLETED
    description = Column(Text)
    metadata_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="logs")
    project = relationship("Project", back_populates="logs")
