import os
import subprocess
import tempfile
import pytest
from database import Database

@pytest.fixture(autouse=True)
def clean_db():
    """Ensure a fresh DB for each CLI test"""
    db_fd, db_path = tempfile.mkstemp()
    os.environ["PLANNER_DB"] = db_path  # override db name
    yield
    os.close(db_fd)
    os.remove(db_path)


def run_cli(args):
    """Helper to run CLI commands and capture output"""
    result = subprocess.run(
        ["python", "planner.py"] + args,
        capture_output=True,
        text=True
    )
    return result.stdout.strip(), result.stderr.strip(), result.returncode


def test_add_and_show_task():
    out, err, code = run_cli(["add", "Test Task", "--duration", "30", "--priority", "high", "--deadline", "2025-09-30"])
    assert code == 0
    assert "Task added" in out

    out, _, _ = run_cli(["show"])
    assert "Test Task" in out


def test_delete_task():
    run_cli(["add", "Temp Task", "--duration", "15", "--priority", "low", "--deadline", "2025-09-25"])
    out, _, _ = run_cli(["show"])
    assert "Temp Task" in out

    run_cli(["delete", "1"])
    out, _, _ = run_cli(["show"])
    assert "No tasks scheduled" in out


def test_add_and_show_reflection():
    out, _, code = run_cli(["reflect", "Great progress today!"])
    assert code == 0
    assert "Reflection saved" in out

    out, _, _ = run_cli(["reflection"])
    assert "Great progress today!" in out
