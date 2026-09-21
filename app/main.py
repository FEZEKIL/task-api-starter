from fastapi import FastAPI, HTTPException, Body, Query
from fastapi.responses import JSONResponse
from typing import Optional, List
import copy

app = FastAPI(title="Task API", version="1.0")

INITIAL_TASKS = [
    {"id": 1, "title": "Buy groceries", "done": False},
    {"id": 2, "title": "Read a book", "done": True},
    {"id": 3, "title": "Write some code", "done": False},
]

tasks = copy.deepcopy(INITIAL_TASKS)

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
    """Returns a list of tasks, optionally filtered by status or search term."""
    filtered_tasks = tasks
    if done is not None:
        filtered_tasks = [t for t in filtered_tasks if t["done"] == done]
    if search is not None:
        filtered_tasks = [t for t in filtered_tasks if search.lower() in t["title"].lower()]
    return filtered_tasks

@app.get("/tasks/{task_id}", summary="Get a single task")
def get_task(task_id: int):
    """Returns a single task by its ID."""
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"}
        )
    return task

@app.post("/tasks", status_code=201, summary="Create a new task")
def create_task(task_data: dict = Body(...)):
    """Creates a new task with the provided title."""
    title = task_data.get("title")
    if not title or not isinstance(title, str) or not title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required and cannot be empty"}
        )

    new_id = max(t["id"] for t in tasks) + 1 if tasks else 1
    new_task = {
        "id": new_id,
        "title": title,
        "done": False
    }
    tasks.append(new_task)
    return new_task

@app.put("/tasks/{task_id}", summary="Update a task")
def update_task(task_id: int, task_data: dict = Body(...)):
    """Updates an existing task's title and/or done status."""
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"}
        )

    title = task_data.get("title")
    done = task_data.get("done")

    if title is None and done is None:
        return JSONResponse(
            status_code=400,
            content={"error": "At least one of 'title' or 'done' must be provided"}
        )

    if title is not None:
        if not isinstance(title, str) or not title.strip():
            return JSONResponse(
                status_code=400,
                content={"error": "Title cannot be empty"}
            )
        task["title"] = title

    if done is not None:
        if not isinstance(done, bool):
            return JSONResponse(
                status_code=400,
                content={"error": "Done must be a boolean"}
            )
        task["done"] = done

    return task

@app.delete("/tasks/{task_id}", status_code=204, summary="Delete a task")
def delete_task(task_id: int):
    """Removes a task from the system."""
    global tasks
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"}
        )
    tasks = [t for t in tasks if t["id"] != task_id]
    return None

@app.get("/stats", summary="Task statistics")
def get_stats():
    """Returns statistics about tasks."""
    total = len(tasks)
    done_count = sum(1 for t in tasks if t["done"])
    return {
        "total": total,
        "done": done_count,
        "open": total - done_count
    }

@app.post("/reset", summary="Reset tasks to initial state")
def reset_tasks():
    """Restores the example tasks and clears all others."""
    global tasks
    tasks = copy.deepcopy(INITIAL_TASKS)
    return {"message": "Tasks reset to initial state"}
