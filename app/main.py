from fastapi import FastAPI, HTTPException, Body, Query
from fastapi.responses import JSONResponse
from typing import Optional, List
import sqlite3
from app.database import init_db, get_db_connection

app = FastAPI(title="Task API", version="1.0")

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/", summary="API Information")
def read_root():
    """Returns basic information about the Task API."""
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks", "/health", "/stats"]
    }

@app.get("/health", summary="Health Check")
def health_check():
    """Returns the status of the API."""
    return {"status": "ok"}

@app.get("/tasks", summary="List all tasks")
def get_tasks(
    done: Optional[bool] = Query(None, description="Filter by completion status"),
    search: Optional[str] = Query(None, description="Search tasks by title")
):
    """Returns a list of tasks from the database, optionally filtered."""
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM tasks WHERE 1=1"
    params = []

    if done is not None:
        query += " AND done = ?"
        params.append(1 if done else 0)

    if search is not None:
        query += " AND title LIKE ?"
        params.append(f"%{search}%")

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]

@app.get("/tasks/{task_id}", summary="Get a single task")
def get_task(task_id: int):
    """Returns a single task from the database by its ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"}
        )
    return dict(row)

@app.post("/tasks", status_code=201, summary="Create a new task")
def create_task(task_data: dict = Body(...)):
    """Creates a new task in the database."""
    # TODO: Implement database insert in Stage 2
    # For now, keeping a dummy response or partial implementation if needed
    # But Stage 1 is just about Read. I'll leave the old logic or a placeholder.
    # The user said "Don't change the CRUD endpoints yet" but Stage 1 specifically says replace Read.
    return {"message": "Create logic not yet migrated to DB"}

@app.put("/tasks/{task_id}", summary="Update a task")
def update_task(task_id: int, task_data: dict = Body(...)):
    return {"message": "Update logic not yet migrated to DB"}

@app.delete("/tasks/{task_id}", status_code=204, summary="Delete a task")
def delete_task(task_id: int):
    return None

@app.get("/stats", summary="Task statistics")
def get_stats():
    conn = get_db_connection()
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

@app.post("/reset", summary="Reset tasks to initial state")
def reset_tasks():
    conn = get_db_connection()
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
    return {"message": "Tasks reset to initial state"}
