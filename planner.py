from database import Database
from datetime import datetime

class Planner:
    def __init__(self):
        self.db = Database()

    def add_task(self, title, duration, priority, deadline):
        """Add a new task into the database"""
        return self.db.add_task(title, duration, priority, deadline)

    def show_tasks(self):
        """Retrieve and print all tasks from the database"""
        tasks = self.db.get_tasks()
        if not tasks:
            print("✅ No tasks scheduled.")
            return

        print("\n📋 Current Tasks:")
        for task in tasks:
            task_id, title, duration, priority, deadline = task
            print(f"  [{task_id}] {title} | {duration} min | {priority} | due {deadline}")

    def delete_task(self, task_id):
        """Remove a task by ID"""
        self.db.delete_task(task_id)
        print(f"🗑️ Task {task_id} deleted.")

    def add_reflection(self, reflection):
        """Add or update today’s reflection"""
        today = datetime.today().strftime("%Y-%m-%d")
        self.db.add_reflection(today, reflection)
        print("✍️ Reflection saved for today.")

    def show_reflection(self, date=None):
        """Show reflection for a given date (default: today)"""
        if not date:
            date = datetime.today().strftime("%Y-%m-%d")
        reflection = self.db.get_reflection(date)
        if reflection:
            print(f"\n📖 Reflection for {date}: {reflection[0]}")
        else:
            print(f"⚠️ No reflection found for {date}.")

    def close(self):
        self.db.close()


# --- Demo Run ---
if __name__ == "__main__":
    planner = Planner()

    # Add tasks
    planner.add_task("Finish CI setup", 60, "high", "2025-09-23")
    planner.add_task("Write database tests", 45, "medium", "2025-09-24")

    # Show tasks
    planner.show_tasks()

    # Add reflection
    planner.add_reflection("Today I integrated SQLite with my planner.")
    planner.show_reflection()

    planner.close()
