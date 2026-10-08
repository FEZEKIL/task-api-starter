from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from app.models import Task
from app.database import get_sqlite_connection, get_db_type

class TaskRepository(ABC):
    @abstractmethod
    def init_db(self) -> None:
        pass

    @abstractmethod
    def get_all(self, done: Optional[bool] = None, search: Optional[str] = None) -> List[Task]:
        pass

    @abstractmethod
    def get_by_id(self, task_id: int) -> Optional[Task]:
        pass

    @abstractmethod
    def create(self, title: str) -> Task:
        pass

    @abstractmethod
    def update(self, task_id: int, title: Optional[str] = None, done: Optional[bool] = None) -> Optional[Task]:
        pass

    @abstractmethod
    def delete(self, task_id: int) -> bool:
        pass

    @abstractmethod
    def get_stats(self) -> Dict[str, int]:
        pass

    @abstractmethod
    def reset(self) -> None:
        pass


class SQLiteTaskRepository(TaskRepository):
    def init_db(self) -> None:
        conn = get_sqlite_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                done BOOLEAN NOT NULL DEFAULT 0
            )
        ''')
        cursor.execute('SELECT COUNT(*) FROM tasks')
        count = cursor.fetchone()[0]

        if count == 0:
            example_tasks = [
                ("Buy groceries", False),
                ("Read a book", True),
                ("Write some code", False)
            ]
            cursor.executemany('INSERT INTO tasks (title, done) VALUES (?, ?)', example_tasks)
            conn.commit()

        conn.close()

    def get_all(self, done: Optional[bool] = None, search: Optional[str] = None) -> List[Task]:
        conn = get_sqlite_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM tasks WHERE 1=1"
        params = []

        if done is not None:
            query += " AND done = ?"
            params.append(1 if done else 0)

        if search is not None:
            query += " AND title LIKE ?"
            params.append(f"%{search}%")

        query += " ORDER BY id ASC"
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        return [Task(id=row["id"], title=row["title"], done=bool(row["done"])) for row in rows]

    def get_by_id(self, task_id: int) -> Optional[Task]:
        conn = get_sqlite_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        conn.close()

        if row is None:
            return None
        return Task(id=row["id"], title=row["title"], done=bool(row["done"]))

    def create(self, title: str) -> Task:
        conn = get_sqlite_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tasks (title, done) VALUES (?, ?)', (title, 0))
        new_id = cursor.lastrowid
        conn.commit()

        cursor.execute('SELECT * FROM tasks WHERE id = ?', (new_id,))
        row = cursor.fetchone()
        conn.close()

        return Task(id=row["id"], title=row["title"], done=bool(row["done"]))

    def update(self, task_id: int, title: Optional[str] = None, done: Optional[bool] = None) -> Optional[Task]:
        conn = get_sqlite_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        task = cursor.fetchone()

        if task is None:
            conn.close()
            return None

        update_fields = []
        params = []
        if title is not None:
            update_fields.append("title = ?")
            params.append(title)

        if done is not None:
            update_fields.append("done = ?")
            params.append(1 if done else 0)

        if update_fields:
            params.append(task_id)
            cursor.execute(f"UPDATE tasks SET {', '.join(update_fields)} WHERE id = ?", params)
            conn.commit()

        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        updated_task = cursor.fetchone()
        conn.close()

        return Task(id=updated_task["id"], title=updated_task["title"], done=bool(updated_task["done"]))

    def delete(self, task_id: int) -> bool:
        conn = get_sqlite_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        if cursor.fetchone() is None:
            conn.close()
            return False

        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()
        return True

    def get_stats(self) -> Dict[str, int]:
        conn = get_sqlite_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM tasks")
        total = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM tasks WHERE done = 1")
        done_count = cursor.fetchone()[0]

        conn.close()

        return {
            "total": total,
            "done": done_count,
            "open": total - done_count
        }

    def reset(self) -> None:
        conn = get_sqlite_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='tasks'")
        example_tasks = [
            ("Buy groceries", False),
            ("Read a book", True),
            ("Write some code", False)
        ]
        cursor.executemany('INSERT INTO tasks (title, done) VALUES (?, ?)', example_tasks)
        conn.commit()
        conn.close()


def get_repository() -> TaskRepository:
    if get_db_type() == "postgres":
        from app.postgres_repository import PostgresTaskRepository
        return PostgresTaskRepository()
    return SQLiteTaskRepository()
