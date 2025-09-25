import pytest
from database import Database

@pytest.fixture
def db():
    # Use an in-memory SQLite DB for testing
    database = Database(":memory:")
    yield database
    database.close()


def test_add_and_get_task(db):
    task_id = db.add_task("Test Task", 30, "medium", "2025-09-30")
    tasks = db.get_tasks()
    assert len(tasks) == 1
    assert tasks[0][0] == task_id
    assert tasks[0][1] == "Test Task"


def test_delete_task(db):
    task_id = db.add_task("Task to Delete", 45, "low", "2025-09-29")
    db.delete_task(task_id)
    tasks = db.get_tasks()
    assert len(tasks) == 0


def test_add_and_get_reflection(db):
    db.add_reflection("2025-09-22", "Learned SQLite integration.")
    reflection = db.get_reflection("2025-09-22")
    assert reflection is not None
    assert "SQLite" in reflection[0]


def test_replace_reflection(db):
    db.add_reflection("2025-09-22", "First entry.")
    db.add_reflection("2025-09-22", "Updated entry.")
    reflection = db.get_reflection("2025-09-22")
    assert reflection[0] == "Updated entry."
