import os
from datetime import datetime
from database import Database

class Planner:
    def __init__(self, db_path=None):
        db_name = db_path or os.environ.get("PLANNER_DB", "planner.db")
        self.db = Database(db_name)

    # TASKS
    def add_task(self, title, duration, priority, deadline):
        query = "INSERT INTO tasks (title, duration, priority, deadline) VALUES (?, ?, ?, ?)"
        cur = self.db.conn.execute(query, (title, duration, priority, deadline))
        self.db.conn.commit()
        task_id = cur.lastrowid
        print(f"Task added with ID {task_id}")
        return task_id

    def show_tasks(self):
        tasks = self.list_tasks()
        if not tasks:
            print("No tasks scheduled.")
            return

        priority_order = {"high": 0, "medium": 1, "low": 2}
        tasks_sorted = sorted(
            tasks,
            key=lambda t: (t[4] or "9999-12-31", priority_order.get(t[3], 1))
        )

        print("\nCurrent Tasks (sorted):")
        for task in tasks_sorted:
            task_id, title, duration, priority, deadline = task
            print(f"  [{task_id}] {title} | {duration} min | {priority} | due {deadline}")

    def delete_task(self, task_id: int):
        self.db.conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        self.db.conn.commit()
        print(f"Task {task_id} deleted.")

    def list_tasks(self):
        return self.db.conn.execute(
            "SELECT id, title, duration, priority, deadline FROM tasks"
        ).fetchall()

    def reschedule_tasks(self):
        today = datetime.today().strftime("%Y-%m-%d")
        tasks = self.list_tasks()
        updated = 0
        for task in tasks:
            task_id, title, duration, priority, deadline = task
            if deadline and deadline < today:
                self.db.conn.execute(
                    "UPDATE tasks SET deadline = ? WHERE id = ?", (today, task_id)
                )
                updated += 1
        self.db.conn.commit()
        print(f"Rescheduled {updated} overdue tasks.")

    # REFLECTIONS
    def add_reflection(self, reflection: str, date: str = None):
        if not date:
            date = datetime.today().strftime("%Y-%m-%d")
        self.db.conn.execute(
            "INSERT INTO reflections (reflection, date) VALUES (?, ?)", (reflection, date)
        )
        self.db.conn.commit()
        print("Reflection saved for today.")

    def list_reflections(self):
        return self.db.conn.execute(
            "SELECT reflection, date FROM reflections ORDER BY date DESC"
        ).fetchall()

    def show_reflection(self, date=None):
        if not date:
            date = datetime.today().strftime("%Y-%m-%d")
        reflection = self.db.get_reflection(date)
        if reflection:
            print(f"\nReflection for {date}: {reflection[0]}")
        else:
            print(f"No reflection found for {date}.")

    def close(self):
        self.db.close()
