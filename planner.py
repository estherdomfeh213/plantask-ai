import json
import os
from datetime import datetime, timedelta


TASKS_FILE = "tasks.json"



def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []  # No file yet → return empty list
    
    with open(TASKS_FILE, "r") as f:
        try:
            return json.load(f)  # Load tasks if JSON is valid
        except json.JSONDecodeError:
            return []  # File is empty or corrupted → reset to empty list

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)  


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



def generate_schedule(start_time="09:00"):
    tasks = sorted(load_tasks(), key=lambda x: (x["priority"], x["deadline"]))
    current_time = datetime.strptime(start_time, "%H:%M")

    print("\n📅 Daily Schedule:")
    for task in tasks:
        if not task["completed"]:
            end_time = current_time + timedelta(minutes=task["duration"])
            print(f"{current_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')} | {task['title']} ({task['priority']})")
            current_time = end_time


def mark_task_done(title):
    tasks = load_tasks()
    for task in tasks:
        if task["title"].lower() == title.lower():
            task["completed"] = True
            print(f"🎯 Task '{title}' marked as complete!")
    save_tasks(tasks)






# Example CLI flow
if __name__ == "__main__":
    while True:
        print("\nPlanTask AI Menu")
        print("1. Add task")
        print("2. Generate schedule")
        print("3. Mark task as done")
        print("4. Exit")

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
            break