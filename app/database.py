import sqlite3
import os

DB_PATH = "tasks.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT 0
        )
    ''')

    # Check if empty
    cursor.execute('SELECT COUNT(*) FROM tasks')
    count = cursor.fetchone()[0]

    if count == 0:
        # Insert example tasks
        example_tasks = [
            ("Buy groceries", False),
            ("Read a book", True),
            ("Write some code", False)
        ]
        cursor.executemany('INSERT INTO tasks (title, done) VALUES (?, ?)', example_tasks)
        conn.commit()

    conn.close()

if __name__ == "__main__":
    init_db()
