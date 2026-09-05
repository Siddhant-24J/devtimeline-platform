import os
import zipfile
import shutil
import math
from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from app.models.models import Project, Milestone, Task

class CodebaseDecomposer:
    """Extracts uploaded ZIP project codebase and decomposes files across user-specified duration (N days)."""

    EXCLUDED_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build", ".next", ".idea", ".vscode"}
    EXCLUDED_EXTENSIONS = {".pyc", ".pyo", ".exe", ".dll", ".so", ".dylib", ".zip", ".tar", ".gz"}

    def extract_and_decompose_zip(
        self,
        zip_file_bytes: bytes,
        project: Project,
        duration_days: int,
        db: Session
    ) -> Dict[str, Any]:
        """Unzips project, analyzes structure, sorts dependency hierarchy, and assigns files to N daily milestones."""

        # 1. Prepare target extraction workspace
        upload_root = os.path.abspath("automation_workspace/uploads")
        project_upload_dir = os.path.join(upload_root, f"project_{project.id}")
        
        if os.path.exists(project_upload_dir):
            shutil.rmtree(project_upload_dir)
        os.makedirs(project_upload_dir, exist_ok=True)

        zip_save_path = os.path.join(project_upload_dir, "source.zip")
        with open(zip_save_path, "wb") as f:
            f.write(zip_file_bytes)

        # Extract ONLY valid source files (skipping node_modules/venv to make extraction 100x faster)
        with zipfile.ZipFile(zip_save_path, "r") as zip_ref:
            for member in zip_ref.infolist():
                # Check if file path contains excluded folder
                path_parts = member.filename.replace("\\", "/").split("/")
                if any(part in self.EXCLUDED_DIRS for part in path_parts):
                    continue
                zip_ref.extract(member, project_upload_dir)

        # 2. Collect & Filter source files
        source_files = []
        for root, dirs, files in os.walk(project_upload_dir):
            # Exclude vendor / build / cache folders
            dirs[:] = [d for d in dirs if d not in self.EXCLUDED_DIRS]
            
            for f in files:
                ext = os.path.splitext(f)[1].lower()
                if ext in self.EXCLUDED_EXTENSIONS or f == "source.zip":
                    continue
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, project_upload_dir)
                source_files.append(rel_path)

        if not source_files:
            source_files = ["README.md", "src/index.js"]

        # 3. Sort files by architectural dependency hierarchy
        # Tier 1: Config, package.json, requirements.txt, models, schema
        # Tier 2: Services, utils, database, core logic
        # Tier 3: API routers, controllers, pages, components
        # Tier 4: Tests, docs, scripts, deployment
        tier1, tier2, tier3, tier4 = [], [], [], []

        for rel in source_files:
            lower = rel.lower()
            if any(k in lower for k in ["config", "package.json", "requirements", "model", "schema", "env", "readme"]):
                tier1.append(rel)
            elif any(k in lower for k in ["service", "util", "db", "database", "core", "helper"]):
                tier2.append(rel)
            elif any(k in lower for k in ["api", "route", "controller", "view", "page", "component"]):
                tier3.append(rel)
            else:
                tier4.append(rel)

        ordered_files = tier1 + tier2 + tier3 + tier4

        # 4. Divide files evenly across N days
        duration_days = max(1, duration_days)
        files_per_day = math.ceil(len(ordered_files) / duration_days)

        created_milestones = []
        for day in range(1, duration_days + 1):
            start_idx = (day - 1) * files_per_day
            end_idx = min(len(ordered_files), day * files_per_day)
            day_files = ordered_files[start_idx:end_idx]

            # If no files left, create placeholder task for final integration
            if not day_files and day > 1:
                day_files = [f"src/integration_day_{day}.py"]

            title = f"Day {day}: Codebase Milestone Implementation"
            if day == 1:
                title = "Day 1: Project Setup, Config & Data Models"
            elif day == duration_days:
                title = f"Day {day}: Integration, Testing & Final Release"

            milestone = Milestone(
                project_id=project.id,
                title=title,
                description=f"Decomposed codebase deliverable for Day {day} containing {len(day_files)} file(s).",
                day_number=day,
                priority="HIGH" if day in (1, duration_days) else "MEDIUM",
                status="PENDING"
            )
            db.add(milestone)
            db.commit()
            db.refresh(milestone)

            # Create tasks for assigned files
            for idx, file_rel in enumerate(day_files, start=1):
                file_name = os.path.basename(file_rel)
                task = Task(
                    milestone_id=milestone.id,
                    title=f"Deploy & Integrate {file_name}",
                    description=f"Implement and validate source deliverable file: {file_rel}",
                    task_type="CODE",
                    status="PENDING",
                    priority="MEDIUM",
                    estimated_minutes=45,
                    files_affected=file_rel
                )
                db.add(task)

            db.commit()
            created_milestones.append(milestone.id)

        project.duration_days = duration_days
        project.status = "ACTIVE"
        db.commit()

        return {
            "total_files": len(ordered_files),
            "duration_days": duration_days,
            "milestones_created": len(created_milestones),
            "upload_dir": project_upload_dir
        }

codebase_decomposer = CodebaseDecomposer()
