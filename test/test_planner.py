import os
import json
import pytest
from datetime import datetime, timedelta
from planner import add_task, load_tasks, save_tasks, reschedule_tasks

TASKS_FILE = "tasks.json"


@pytest.fixture(autouse=True)
def clean_tasks():
    """Reset tasks.json before each test"""
    if os.path.exists(TASKS_FILE):
        os.remove(TASKS_FILE)
    yield
    if os.path.exists(TASKS_FILE):
        os.remove(TASKS_FILE)


def test_add_task():
    add_task("Write report", 60, "high", "2025-09-23")
    tasks = load_tasks()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Write report"
    assert tasks[0]["priority"] == "high"


def test_reschedule_task():
    yesterday = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    add_task("Missed task", 30, "medium", yesterday)

    reschedule_tasks()
    tasks = load_tasks()

    assert tasks[0]["rescheduled"] is True
    assert datetime.strptime(tasks[0]["deadline"], "%Y-%m-%d").date() > datetime.today().date()


def test_save_and_load():
    tasks = [{"title": "Dummy", "duration": 15, "priority": "low", "deadline": "2025-09-25", "completed": False}]
    save_tasks(tasks)
    loaded = load_tasks()
    assert loaded == tasks
