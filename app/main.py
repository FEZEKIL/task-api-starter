from fastapi import FastAPI, Body, Query, Request, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional, List
from contextlib import asynccontextmanager

from app.services import TaskService
from app.auth import auth_router, public_router, protected_router

task_service = TaskService()

@asynccontextmanager
async def lifespan(app: FastAPI):
    task_service.init_db()
    yield

app = FastAPI(
    title="Task API",
    version="1.0",
    description="Containerized CRUD REST API with Supabase Authentication and Repository Pattern storage abstraction.",
    lifespan=lifespan
)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if isinstance(exc.detail, dict) and "error" in exc.detail:
        return JSONResponse(status_code=exc.status_code, content=exc.detail)
    return JSONResponse(status_code=exc.status_code, content={"error": str(exc.detail)})

# Include Auth & Public/Protected Routers
app.include_router(auth_router)
app.include_router(public_router)
app.include_router(protected_router)

@app.get("/", summary="API Information")
def read_root():
    """Returns basic information about the Task API."""
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": [
            "/tasks", "/health", "/stats",
            "/auth/signup", "/auth/login", "/auth/logout",
            "/public/info", "/protected/profile", "/protected/dashboard"
        ]
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
    return task_service.list_tasks(done=done, search=search)

@app.get("/tasks/{task_id}", summary="Get a single task")
def get_task(task_id: int):
    """Returns a single task from the database by its ID."""
    task = task_service.get_task(task_id)
    if task is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"}
        )
    return task

@app.post("/tasks", status_code=201, summary="Create a new task")
def create_task(task_data: dict = Body(...)):
    """Creates a new task in the database."""
    title = task_data.get("title")
    if not title or not isinstance(title, str) or not title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required and cannot be empty"}
        )

    return task_service.create_task(title.strip())

@app.put("/tasks/{task_id}", summary="Update a task")
def update_task(task_id: int, task_data: dict = Body(...)):
    """Updates an existing task in the database."""
    existing_task = task_service.get_task(task_id)
    if existing_task is None:
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
        title = title.strip()

    if done is not None:
        if not isinstance(done, bool):
            return JSONResponse(
                status_code=400,
                content={"error": "Done must be a boolean"}
            )

    updated_task = task_service.update_task(task_id, title=title, done=done)
    return updated_task

@app.delete("/tasks/{task_id}", status_code=204, summary="Delete a task")
def delete_task(task_id: int):
    """Removes a task from the database."""
    deleted = task_service.delete_task(task_id)
    if not deleted:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"}
        )
    return None

@app.get("/stats", summary="Task statistics")
def get_stats():
    return task_service.get_stats()

@app.post("/reset", summary="Reset tasks to initial state")
def reset_tasks():
    task_service.reset_tasks()
    return {"message": "Tasks reset to initial state"}
