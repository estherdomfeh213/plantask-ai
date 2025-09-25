import argparse
from datetime import datetime
from database import Database
import os

class Planner:
    def __init__(self):
        db_name = os.environ.get("PLANNER_DB", "planner.db")
        self.db = Database(db_name)

    def add_task(self, title, duration, priority, deadline):
        task_id = self.db.add_task(title, duration, priority, deadline)
        print(f"Task added with ID {task_id}")

    def show_tasks(self):
        tasks = self.db.get_tasks()
        if not tasks:
            print("No tasks scheduled.")
            return
        print("\nCurrent Tasks:")
        for task in tasks:
            task_id, title, duration, priority, deadline = task
            print(f"  [{task_id}] {title} | {duration} min | {priority} | due {deadline}")

    def delete_task(self, task_id):
        self.db.delete_task(task_id)
        print(f"Task {task_id} deleted.")

    def add_reflection(self, reflection):
        today = datetime.today().strftime("%Y-%m-%d")
        self.db.add_reflection(today, reflection)
        print(" Reflection saved for today.")

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


def main():
    parser = argparse.ArgumentParser(description="PlanTask AI CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Add Task
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", type=str, help="Task title")
    add_parser.add_argument("--duration", type=int, default=60, help="Task duration in minutes")
    add_parser.add_argument("--priority", type=str, default="medium", choices=["low", "medium", "high"])
    add_parser.add_argument("--deadline", type=str, help="Deadline (YYYY-MM-DD)")

    # Show Tasks
    subparsers.add_parser("show", help="Show all tasks")

    # Delete Task
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("task_id", type=int, help="Task ID to delete")

    # Add Reflection
    reflect_parser = subparsers.add_parser("reflect", help="Add today’s reflection")
    reflect_parser.add_argument("reflection", type=str, help="Reflection text")

    # Show Reflection
    reflection_parser = subparsers.add_parser("reflection", help="Show reflection for a date (default: today)")
    reflection_parser.add_argument("--date", type=str, help="Date (YYYY-MM-DD)")

    args = parser.parse_args()
    planner = Planner()

    if args.command == "add":
        planner.add_task(args.title, args.duration, args.priority, args.deadline)
    elif args.command == "show":
        planner.show_tasks()
    elif args.command == "delete":
        planner.delete_task(args.task_id)
    elif args.command == "reflect":
        planner.add_reflection(args.reflection)
    elif args.command == "reflection":
        planner.show_reflection(args.date)
    else:
        parser.print_help()

    planner.close()


if __name__ == "__main__":
    main()
