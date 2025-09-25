import sqlite3
from datetime import datetime

DB_NAME = "planner.db"

class Database:
    def __init__(self, db_name=DB_NAME):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()

        # Tasks table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            duration INTEGER,
            priority TEXT,
            deadline DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Reflections table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS reflections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE UNIQUE,
            reflection TEXT
        )
        """)

        self.conn.commit()

    # --- Task Methods ---
    def add_task(self, title, duration, priority, deadline):
        cursor = self.conn.cursor()
        cursor.execute("""
        INSERT INTO tasks (title, duration, priority, deadline)
        VALUES (?, ?, ?, ?)
        """, (title, duration, priority, deadline))
        self.conn.commit()
        return cursor.lastrowid

    def get_tasks(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, title, duration, priority, deadline FROM tasks ORDER BY deadline")
        return cursor.fetchall()

    def delete_task(self, task_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.conn.commit()

    # --- Reflection Methods ---
    def add_reflection(self, date, reflection):
        cursor = self.conn.cursor()
        cursor.execute("""
        INSERT OR REPLACE INTO reflections (date, reflection)
        VALUES (?, ?)
        """, (date, reflection))
        self.conn.commit()

    def get_reflection(self, date):
        cursor = self.conn.cursor()
        cursor.execute("SELECT reflection FROM reflections WHERE date = ?", (date,))
        return cursor.fetchone()

    def close(self):
        self.conn.close()


# --- Demo Run ---
if __name__ == "__main__":
    db = Database()

    # Add a task
    task_id = db.add_task("Finish AI project", 120, "high", "2025-09-25")
    print(f"Task added with ID {task_id}")

    # List tasks
    tasks = db.get_tasks()
    print("All Tasks:", tasks)

    # Add reflection
    db.add_reflection(datetime.today().strftime("%Y-%m-%d"), "Good progress today!")
    reflection = db.get_reflection(datetime.today().strftime("%Y-%m-%d"))
    print("Reflection:", reflection)

    db.close()
