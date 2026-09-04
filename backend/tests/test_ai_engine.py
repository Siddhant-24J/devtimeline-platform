import os
import pytest
from app.services.ai_engine import AIDevelopmentEngine
from app.models.models import Task

def test_ai_architecture_analysis(tmp_path):
    engine = AIDevelopmentEngine()
    # Create sample files
    f1 = tmp_path / "app.py"
    f1.write_text("print('hello world')")

    analysis = engine.analyze_codebase_architecture(str(tmp_path))
    assert analysis["total_files"] == 1
    assert "Python" in analysis["detected_languages"]
    assert len(analysis["architectural_insights"]) > 0

def test_ai_code_implementation_synthesis():
    engine = AIDevelopmentEngine()
    task = Task(id=42, title="Build User Auth Service", task_type="BACKEND", description="JWT User Auth")

    rel_file, code = engine.generate_code_implementation(task, "", "app/services/auth.py")
    assert rel_file == "app/services/auth.py"
    assert "BuildUserAuthService" in code or "class" in code
    assert "def process_task_execution" in code

def test_ai_unit_test_generation():
    engine = AIDevelopmentEngine()
    task = Task(id=42, title="Build User Auth Service", task_type="BACKEND")

    test_file, test_code = engine.generate_unit_tests(task, "app/services/auth.py")
    assert "test_auth.py" in test_file
    assert "import pytest" in test_code
    assert "test_service_initialization" in test_code

def test_ai_self_healing_repair_loop(tmp_path):
    engine = AIDevelopmentEngine()
    buggy_file = tmp_path / "buggy.py"
    buggy_file.write_text("def broken_func()\n    return 42\n")

    success, msg, repaired = engine.self_healing_repair_loop(
        repo_path=str(tmp_path),
        file_target="buggy.py",
        error_msg="SyntaxError: invalid syntax"
    )

    assert success is True
    assert "def broken_func():" in repaired

def test_ai_project_documentation_generator(tmp_path):
    engine = AIDevelopmentEngine()
    docs = engine.generate_project_documentation(str(tmp_path), "Test AI Project")
    assert docs["readme_file"] == "README.md"
    assert "Test AI Project" in docs["content"]
