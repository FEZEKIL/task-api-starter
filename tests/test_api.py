from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_get_tasks():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) == 3

def test_get_single_task():
    response = client.get("/tasks/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_get_task_not_found():
    response = client.get("/tasks/99")
    assert response.status_code == 404
    assert response.json() == {"error": "Task 99 not found"}

def test_create_task():
    response = client.post("/tasks", json={"title": "Buy milk"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Buy milk"
    assert data["done"] is False

def test_create_task_invalid():
    response = client.post("/tasks", json={})
    assert response.status_code == 400
    assert "error" in response.json()
