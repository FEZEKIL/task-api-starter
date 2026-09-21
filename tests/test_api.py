from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["name"] == "Task API"

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_get_tasks():
    client.post("/reset")
    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) == 3

def test_get_single_task():
    client.post("/reset")
    response = client.get("/tasks/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_get_task_not_found():
    response = client.get("/tasks/99")
    assert response.status_code == 404

def test_create_task():
    client.post("/reset")
    response = client.post("/tasks", json={"title": "Buy milk"})
    assert response.status_code == 201
    assert response.json()["title"] == "Buy milk"

def test_create_task_invalid():
    response = client.post("/tasks", json={})
    assert response.status_code == 400

def test_update_task():
    client.post("/reset")
    response = client.put("/tasks/1", json={"title": "Updated", "done": True})
    assert response.status_code == 200
    assert response.json()["done"] is True

def test_delete_task():
    client.post("/reset")
    response = client.delete("/tasks/1")
    assert response.status_code == 204

def test_stats():
    client.post("/reset")
    response = client.get("/stats")
    assert response.status_code == 200
    assert response.json()["total"] == 3

def test_reset():
    client.post("/tasks", json={"title": "Temp"})
    client.post("/reset")
    response = client.get("/tasks")
    assert len(response.json()) == 3
