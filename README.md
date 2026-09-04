# DevTimeline — AI-Powered Project Development Planner & GitHub Automation Platform

DevTimeline turns existing codebases, uploaded projects, or built-in project templates into structured, dependency-aware development plans and automates daily progress commits directly to GitHub.

---

## 🌟 Key Features

* **3 Ingestion Sources**:
  * Existing GitHub repository
  * Upload ZIP archive
  * Built-in Project Library (Beginner, Intermediate, Advanced)
* **Automated Project Analysis**: Detects languages, frameworks, DB models, test suites, and project architecture.
* **Dependency-Aware Roadmap Generator**: Breaks projects down into logical daily milestones (7, 14, 30, 60, 90 days).
* **Automated Task Execution Engine**: Executes daily coding, testing, and documentation tasks with isolated branch sandboxing.
* **Automated GitHub Synchronization**: Pushes validated, meaningful commits directly to your GitHub repository.
* **Interactive Dashboard**: Track timeline progression, commit velocity, execution logs, and project health.

---

## 🛠️ Architecture & Tech Stack

* **Frontend**: Next.js 14 / React (TypeScript), Tailwind CSS, Lucide Icons
* **Backend**: FastAPI (Python 3.10+), Pydantic, SQLAlchemy
* **Database**: SQLite (Dev) / PostgreSQL (Prod)
* **Integrations**: GitHub App OAuth & REST API

---

## 📁 Repository Structure

```text
.
├── backend/              # FastAPI Backend API & Database Services
├── frontend/             # Next.js Web Frontend & UI Components
├── project-library/      # Pre-configured project templates & roadmaps
├── automation/           # Task runner, code validator & git execution sandbox
├── database/             # Alembic migrations & seed scripts
├── DevTimeline_Complete_Project_Specification.md # Complete Specification
└── README.md
```

---

## 🚀 Quick Start

### 1. Backend Setup

```bash
cd backend
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
python -m app.scripts.seed_projects
uvicorn app.main:app --reload --port 8000
```

FastAPI Documentation will be available at `http://127.0.0.1:8000/docs`.

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend UI will be available at `http://localhost:3000`.

---

## 📄 License

MIT License. Developed for genuine software orchestration.
