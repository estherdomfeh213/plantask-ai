import os
import tempfile
import pytest
from fastapi.testclient import TestClient

# Point the app to a temporary DB for tests
os.environ["PLANNER_DB"] = tempfile.mktemp()

from webapp.main import app, get_planner
from planner import Planner

client = TestClient(app)

@pytest.fixture(autouse=True)
def clean_db():
    """Ensure a clean DB for each test."""
    db_path = os.environ["PLANNER_DB"]
    if os.path.exists(db_path):
        os.remove(db_path)
    yield
    if os.path.exists(db_path):
        os.remove(db_path)

def test_homepage_loads():
    response = client.get("/")
    assert response.status_code == 200
    assert "PlanTask AI" in response.text

def test_add_and_list_task():
    response = client.post("/add", data={
        "title": "Test Task",
        "duration": 45,
        "priority": "high",
        "deadline": "2025-09-30"
    })
    assert response.status_code == 303

    # check if task appears
    response = client.get("/")
    assert "Test Task" in response.text
    assert "45 min" in response.text
    assert "high" in response.text

def test_delete_task():
    # add task first
    client.post("/add", data={
        "title": "Delete Me",
        "duration": 30,
        "priority": "low",
        "deadline": "2025-09-29"
    })

    # find task in HTML
    response = client.get("/")
    assert "Delete Me" in response.text

    # delete task (assume ID = 1 since DB is clean)
    response = client.post("/delete/1")
    assert response.status_code == 303

    # confirm task gone
    response = client.get("/")
    assert "Delete Me" not in response.text

def test_add_reflection():
    response = client.post("/reflections", data={"entry": "Great progress today!"})
    assert response.status_code == 303

    # check if reflection is listed
    response = client.get("/reflections")
    assert "Great progress today!" in response.text

def test_reschedule_task():
    # Add overdue task
    client.post("/add", data={
        "title": "Overdue Task",
        "duration": 20,
        "priority": "medium",
        "deadline": "2020-01-01"
    })

    # trigger reschedule
    response = client.post("/reschedule")
    assert response.status_code == 303

    # check if deadline updated
    response = client.get("/")
    assert "Overdue Task" in response.text
    assert "2020-01-01" not in response.text  # deadline should change
