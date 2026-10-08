from typing import Optional, List, Dict, Any
from app.models import Task
from app.repository import TaskRepository
from app.database import get_postgres_connection

class PostgresTaskRepository(TaskRepository):
    def init_db(self) -> None:
        conn = get_postgres_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                done BOOLEAN NOT NULL DEFAULT FALSE
            )
        ''')
        cursor.execute('SELECT COUNT(*) FROM tasks')
        res = cursor.fetchone()
        count = res['count'] if res else 0

        if count == 0:
            example_tasks = [
                ("Buy groceries", False),
                ("Read a book", True),
                ("Write some code", False)
            ]
            for title, done in example_tasks:
                cursor.execute('INSERT INTO tasks (title, done) VALUES (%s, %s)', (title, done))
            conn.commit()

        cursor.close()
        conn.close()

    def get_all(self, done: Optional[bool] = None, search: Optional[str] = None) -> List[Task]:
        conn = get_postgres_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM tasks WHERE 1=1"
        params = []

        if done is not None:
            query += " AND done = %s"
            params.append(done)

        if search is not None:
            query += " AND title ILIKE %s"
            params.append(f"%{search}%")

        query += " ORDER BY id ASC"
        cursor.execute(query, params)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        return [Task(id=row["id"], title=row["title"], done=bool(row["done"])) for row in rows]

    def get_by_id(self, task_id: int) -> Optional[Task]:
        conn = get_postgres_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if row is None:
            return None
        return Task(id=row["id"], title=row["title"], done=bool(row["done"]))

    def create(self, title: str) -> Task:
        conn = get_postgres_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING id, title, done", (title, False))
        row = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()

        return Task(id=row["id"], title=row["title"], done=bool(row["done"]))

    def update(self, task_id: int, title: Optional[str] = None, done: Optional[bool] = None) -> Optional[Task]:
        conn = get_postgres_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
        task = cursor.fetchone()

        if task is None:
            cursor.close()
            conn.close()
            return None

        update_fields = []
        params = []
        if title is not None:
            update_fields.append("title = %s")
            params.append(title)

        if done is not None:
            update_fields.append("done = %s")
            params.append(done)

        if update_fields:
            params.append(task_id)
            cursor.execute(f"UPDATE tasks SET {', '.join(update_fields)} WHERE id = %s RETURNING id, title, done", params)
            updated_task = cursor.fetchone()
            conn.commit()
        else:
            updated_task = task

        cursor.close()
        conn.close()

        return Task(id=updated_task["id"], title=updated_task["title"], done=bool(updated_task["done"]))

    def delete(self, task_id: int) -> bool:
        conn = get_postgres_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
        if cursor.fetchone() is None:
            cursor.close()
            conn.close()
            return False

        cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True

    def get_stats(self) -> Dict[str, int]:
        conn = get_postgres_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) as total FROM tasks")
        total = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) as done_count FROM tasks WHERE done = TRUE")
        done_count = cursor.fetchone()["done_count"]

        cursor.close()
        conn.close()

        return {
            "total": total,
            "done": done_count,
            "open": total - done_count
        }

    def reset(self) -> None:
        conn = get_postgres_connection()
        cursor = conn.cursor()
        cursor.execute("TRUNCATE TABLE tasks RESTART IDENTITY")
        example_tasks = [
            ("Buy groceries", False),
            ("Read a book", True),
            ("Write some code", False)
        ]
        for title, done in example_tasks:
            cursor.execute('INSERT INTO tasks (title, done) VALUES (%s, %s)', (title, done))
        conn.commit()
        cursor.close()
        conn.close()
