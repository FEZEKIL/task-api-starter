from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import JSONResponse

app = FastAPI()

tasks = [
    {"id": 1, "title": "Buy groceries", "done": False},
    {"id": 2, "title": "Read a book", "done": True},
    {"id": 3, "title": "Write some code", "done": False},
]

@app.get("/")
def read_root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"}
        )
    return task

@app.post("/tasks", status_code=201)
def create_task(task_data: dict = Body(...)):
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

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_data: dict = Body(...)):
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

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    global tasks
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"}
        )
    tasks = [t for t in tasks if t["id"] != task_id]
    return None
