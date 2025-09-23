import sys, os
import re
from datetime import datetime, timedelta
#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
#from ai_parser import parse_task_input
from ai_parser import parse_task_input



def test_basic_task():
    result = parse_task_input("Write essay tomorrow, high priority, 2 hours")
    assert result["title"].lower().startswith("write essay")
    assert result["priority"] == "high"
    assert result["duration"] == 120
    assert result["deadline"] == (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")


def test_minutes_duration():
    result = parse_task_input("Read article today, 30 minutes, low priority")
    assert result["duration"] == 30
    assert result["priority"] == "low"
    assert result["deadline"] == datetime.today().strftime("%Y-%m-%d")


def test_default_values():
    result = parse_task_input("Brainstorm project ideas")
    assert result["priority"] == "medium"
    assert result["duration"] == 60
    assert re.match(r"\d{4}-\d{2}-\d{2}", result["deadline"])
    assert "brainstorm" in result["title"].lower()
