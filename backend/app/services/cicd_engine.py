import os
from typing import Dict, Any, Tuple

class CICDEngine:
    """Generates production-grade Dockerfile, docker-compose.yml, and GitHub Actions workflow pipelines."""

    def generate_dockerfile(self, repo_path: str, tech_stack: str = "Python") -> Tuple[str, str]:
        """Generates Dockerfile tailored to the project tech stack."""
        if "Python" in tech_stack or "FastAPI" in tech_stack:
            content = (
                "# Production Dockerfile for FastAPI Backend\n"
                "FROM python:3.11-slim\n\n"
                "WORKDIR /app\n\n"
                "COPY requirements.txt .\n"
                "RUN pip install --no-cache-dir -r requirements.txt\n\n"
                "COPY . .\n\n"
                "EXPOSE 8000\n"
                "CMD [\"uvicorn\", \"app.main:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]\n"
            )
        else:
            content = (
                "# Production Dockerfile for Node.js / Next.js\n"
                "FROM node:18-alpine\n\n"
                "WORKDIR /app\n\n"
                "COPY package*.json .\n"
                "RUN npm install --production\n\n"
                "COPY . .\n\n"
                "EXPOSE 3000\n"
                "CMD [\"npm\", \"start\"]\n"
            )

        dockerfile_path = os.path.join(repo_path, "Dockerfile")
        if os.path.exists(repo_path):
            with open(dockerfile_path, "w", encoding="utf-8") as f:
                f.write(content)

        return "Dockerfile", content

    def generate_docker_compose(self, repo_path: str) -> Tuple[str, str]:
        """Generates docker-compose.yml for local multi-container development."""
        content = (
            "version: '3.8'\n\n"
            "services:\n"
            "  web:\n"
            "    build: .\n"
            "    ports:\n"
            "      - '8000:8000'\n"
            "    environment:\n"
            "      - DATABASE_URL=sqlite:///./devtimeline.db\n"
            "    restart: always\n"
        )
        compose_path = os.path.join(repo_path, "docker-compose.yml")
        if os.path.exists(repo_path):
            with open(compose_path, "w", encoding="utf-8") as f:
                f.write(content)

        return "docker-compose.yml", content

    def generate_github_actions_workflow(self, repo_path: str) -> Tuple[str, str]:
        """Generates .github/workflows/devtimeline-ci.yml for automated CI testing and linting."""
        content = (
            "name: DevTimeline CI Pipeline\n\n"
            "on:\n"
            "  push:\n"
            "    branches: [ main, 'devtimeline/*' ]\n"
            "  pull_request:\n"
            "    branches: [ main ]\n\n"
            "jobs:\n"
            "  test-and-lint:\n"
            "    runs-on: ubuntu-latest\n"
            "    steps:\n"
            "      - uses: actions/checkout@v3\n"
            "      - name: Set up Python\n"
            "        uses: actions/setup-python@v4\n"
            "        with:\n"
            "          python-version: '3.11'\n"
            "      - name: Install dependencies\n"
            "        run: |\n"
            "          python -m pip install --upgrade pip\n"
            "          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi\n"
            "      - name: Run Test Suite\n"
            "        run: |\n"
            "          python -m pytest tests/\n"
        )

        wf_dir = os.path.join(repo_path, ".github", "workflows")
        wf_path = os.path.join(wf_dir, "devtimeline-ci.yml")

        if os.path.exists(repo_path):
            os.makedirs(wf_dir, exist_ok=True)
            with open(wf_path, "w", encoding="utf-8") as f:
                f.write(content)

        return ".github/workflows/devtimeline-ci.yml", content

cicd_engine = CICDEngine()
