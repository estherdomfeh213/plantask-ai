import os
import tempfile
from planner import Planner
from datetime import datetime, timedelta

def test_reschedule_moves_overdue_tasks():
    db_fd, db_path = tempfile.mkstemp()
    os.environ["PLANNER_DB"] = db_path
    planner = Planner()

    # yesterday
    yesterday = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    planner.add_task("Overdue Task", 30, "high", yesterday)

    # run reschedule
    planner.reschedule_tasks()

    tasks = planner.db.get_tasks()
    today = datetime.today().strftime("%Y-%m-%d")
    assert tasks[0][4] == today  # deadline updated

    planner.close()
    os.close(db_fd)
    os.remove(db_path)
