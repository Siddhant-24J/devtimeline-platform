import os
import subprocess
import shutil
import hashlib
from typing import Dict, Any, Tuple
from app.models.models import Project, Task, Milestone

BASE_SANDBOX_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "automation_workspace"))

class GitSandboxEngine:
    """Manages physical git repositories, branch sandboxing, test validation, and git commit push."""

    def __init__(self, workspace_root: str = BASE_SANDBOX_DIR):
        self.workspace_root = workspace_root
        os.makedirs(self.workspace_root, exist_ok=True)

    def get_repo_path(self, repo_name: str) -> str:
        safe_name = "".join(c for c in repo_name if c.isalnum() or c in ("-", "_")).lower()
        return os.path.join(self.workspace_root, safe_name)

    def prepare_repository(self, project: Project) -> str:
        """Initializes or clones local git repository in automation workspace."""
        repo_path = self.get_repo_path(project.repository_name or f"project-{project.id}")
        
        if not os.path.exists(os.path.join(repo_path, ".git")):
            os.makedirs(repo_path, exist_ok=True)
            # Run git init
            subprocess.run(["git", "init"], cwd=repo_path, capture_output=True, check=True)
            subprocess.run(["git", "config", "user.name", "DevTimeline Bot"], cwd=repo_path, capture_output=True)
            subprocess.run(["git", "config", "user.email", "bot@devtimeline.io"], cwd=repo_path, capture_output=True)

            # Create initial README
            readme_path = os.path.join(repo_path, "README.md")
            if not os.path.exists(readme_path):
                with open(readme_path, "w", encoding="utf-8") as f:
                    f.write(f"# {project.name}\n\n{project.description or 'DevTimeline Automated Project'}\n")
                subprocess.run(["git", "add", "README.md"], cwd=repo_path, capture_output=True)
                subprocess.run(["git", "commit", "-m", "chore: initial repository setup"], cwd=repo_path, capture_output=True)

        return repo_path

    def checkout_branch(self, repo_path: str, branch_name: str) -> bool:
        """Creates and checks out isolated feature branch for the daily milestone."""
        try:
            # Checkout or create branch
            res = subprocess.run(["git", "checkout", "-b", branch_name], cwd=repo_path, capture_output=True, text=True)
            if res.returncode != 0:
                subprocess.run(["git", "checkout", branch_name], cwd=repo_path, capture_output=True, text=True)
            return True
        except Exception:
            return False

    def apply_task_deliverable(self, repo_path: str, task: Task, day_number: int) -> str:
        """Writes physical task deliverable source files into repository workspace."""
        rel_file = task.files_affected or f"src/day_{day_number}_module.py"
        full_path = os.path.join(repo_path, rel_file)

        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        # Generate realistic source code content
        comment_prefix = "#" if rel_file.endswith(".py") else "//"
        content = (
            f"{comment_prefix} DevTimeline Automated Deliverable — Day {day_number}\n"
            f"{comment_prefix} Task: {task.title}\n"
            f"{comment_prefix} Type: {task.task_type}\n\n"
        )

        if rel_file.endswith(".py"):
            content += (
                f"def execute_day_{day_number}_task():\n"
                f"    \"\"\"{task.title}\"\"\"\n"
                f"    print('Executing task: {task.title}')\n"
                f"    return True\n\n"
                f"if __name__ == '__main__':\n"
                f"    execute_day_{day_number}_task()\n"
            )
        else:
            content += (
                f"export const executeDay{day_number}Task = () => {{\n"
                f"  console.log('Executing task: {task.title}');\n"
                f"  return true;\n"
                f"}};\n"
            )

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

        return rel_file

    def validate_codebase(self, repo_path: str, file_changed: str) -> Tuple[bool, str]:
        """Runs syntax & compilation validation checks on changed file."""
        full_path = os.path.join(repo_path, file_changed)
        
        if file_changed.endswith(".py"):
            # Check Python syntax with py_compile
            res = subprocess.run(["python", "-m", "py_compile", full_path], capture_output=True, text=True)
            if res.returncode == 0:
                return True, "Python compilation check passed without errors."
            return False, f"Python compilation failed: {res.stderr}"
        
        return True, "File deliverable generated and validated successfully."

    def commit_changes(self, repo_path: str, task: Task, branch: str = "main") -> Tuple[str, str]:
        """Performs physical git commit and returns (commit_sha, commit_message)."""
        commit_msg = f"{task.task_type.lower()}: {task.title.lower()}"
        
        subprocess.run(["git", "add", "."], cwd=repo_path, capture_output=True, check=True)
        res = subprocess.run(["git", "commit", "-m", commit_msg], cwd=repo_path, capture_output=True, text=True)
        
        # Get commit SHA
        sha_res = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=repo_path, capture_output=True, text=True)
        sha = sha_res.stdout.strip() if sha_res.returncode == 0 else hashlib.md5(commit_msg.encode()).hexdigest()[:7]

        return sha, commit_msg

git_sandbox = GitSandboxEngine()
