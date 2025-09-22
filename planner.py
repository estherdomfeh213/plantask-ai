import json
import os
from datetime import datetime, timedelta


TASKS_FILE = "tasks.json"



def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []  # No file yet, return empty list
    
    with open(TASKS_FILE, "r") as f:
        try:
            return json.load(f)  # Load tasks if JSON is valid
        except json.JSONDecodeError:
            return []  # File is empty or corrupted,  reset to empty list

def save_tasks(tasks):
    def default(o):
        if isinstance(o, datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        return str(o)
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4, default=default)


def add_task(title, duration, priority, deadline):
    tasks = load_tasks()
    task = {
        "title": title,
        "duration": duration,   # in minutes
        "priority": priority, # high, medium, low 
        "deadline": deadline,  # YYYY-MM-DD
        "completed": False 
    }

    tasks. append(task)
    save_tasks(tasks)
    print(f"✅ Task '{title} added!")



def generate_schedule(start_time="09:00", end_time="18:00"):
    tasks = load_tasks()

    # Map priority to weights
    priority_map = {"high": 1, "medium": 2, "low": 3}

    # Convert deadlines to datetime for sorting
    for task in tasks:
        task["deadline_dt"] = datetime.strptime(task["deadline"], "%Y-%m-%d")

    # Sort tasks by (deadline, priority weight, duration)
    tasks = sorted(
        tasks,
        key=lambda x: (
            x["deadline_dt"],
            priority_map.get(x["priority"], 3),
            x["duration"]
        )
    )

    current_time = datetime.strptime(start_time, "%H:%M")
    end_time = datetime.strptime(end_time, "%H:%M")

    print("\n📅 Optimized Daily Schedule:")
    for task in tasks:
        if not task["completed"]:
            task_deadline = task["deadline_dt"].date()

            # If deadline is today, force priority
            if task_deadline == datetime.today().date():
                task_priority = "URGENT"
            else:
                task_priority = task["priority"]

            end_slot = current_time + timedelta(minutes=task["duration"])

            # If schedule exceeds workday then move to next day
            if end_slot > end_time:
                print(f"⚠️ Not enough time for '{task['title']}' today. Rescheduling...")
                new_deadline = datetime.today().date() + timedelta(days=1)
                task["deadline"] = new_deadline.strftime("%Y-%m-%d")
                task["rescheduled"] = True
                continue

            print(f"{current_time.strftime('%H:%M')} - {end_slot.strftime('%H:%M')} | {task['title']} ({task_priority})")

            current_time = end_slot

    save_tasks(tasks)



def mark_task_done(title):
    tasks = load_tasks()
    for task in tasks:
        if task["title"].lower() == title.lower():
            task["completed"] = True
            print(f"🎯 Task '{title}' marked as complete!")
    save_tasks(tasks)


def reschedule_tasks():
    """Moves unfinished tasks automatically roll over to the next day"""
    tasks = load_tasks()
    today = datetime.today().date()

    for task in tasks:
        if not task["completed"]:
            deadline_date = datetime.strptime(task["deadline"], "%Y-%m-%d").date()
            if deadline_date < today:
                new_deadline = today + timedelta(days=1)
                task["deadline"] = new_deadline.strftime("%Y-%m-%d")
                task["rescheduled"] = True
                print(f"🔄 Task '{task['title']}' rescheduled to {task['deadline']}")

    save_tasks(tasks)

def daily_reflection():
    """Shows completed, pending, and resheduling tasks for the day """
    tasks = load_tasks()
    today = datetime.today().date()

    completed = [t["title"] for t in tasks if t["completed"]]
    pending = [t["title"] for t in tasks if not t["completed"] and t["deadline"] == today.strftime("%Y-%m-%d")]
    rescheduled = [t["title"] for t in tasks if t.get("rescheduled", False)]


    print("\n✨ Daily Reflection ✨")
    print("\n✅ Completed Tasks:")
    for t in completed:
        print(f" - {t}")

    print("\n⏳ Pending Tasks:")
    for t in pending:
        print(f" - {t}")

    print("\n🔄 Rescheduled Tasks:")
    for t in rescheduled:
        print(f" - {t}")



# Sample CLI flow
if __name__ == "__main__":
    while True:
        print("\nPlanTask AI Menu")
        print("1. Add task")
        print("2. Generate schedule")
        print("3. Mark task as done")
        print("4. Reschedule missed tasks")
        print("5. Daily reflection")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            title = input("Task title: ")
            duration = int(input("Duration (minutes): "))
            priority = input("Priority (high/medium/low): ")
            deadline = input("Deadline (YYYY-MM-DD): ")
            add_task(title, duration, priority, deadline)

        elif choice == "2":
            generate_schedule()

        elif choice == "3":
            title = input("Enter task title to mark as done: ")
            mark_task_done(title)

        elif choice == "4":
            reschedule_tasks()

        elif choice == "5":
            daily_reflection()


        elif choice == "6":
            break