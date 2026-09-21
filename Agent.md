# Agent Instructions

## Project

Task API — FlyRank Backend AI Engineering BE-01.

This repository implements a small CRUD API using Python and FastAPI.

## Primary Goal

Build and publish a fully functional in-memory task management API.

## Technology

- Python 3.10+
- FastAPI
- Uvicorn
- pytest
- Swagger/OpenAPI via FastAPI

## Important Constraints

1. Tasks must remain in memory.
2. Do not add a database.
3. Do not add file persistence.
4. Restarting the server must reset the task list.
5. Required endpoints must remain available.
6. Required HTTP status codes must not be changed.
7. Validation errors must return JSON containing `error`.
8. Swagger UI must remain available at `/docs`.

## Required Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | API information |
| GET | `/health` | Health check |
| GET | `/tasks` | List tasks |
| GET | `/tasks/{id}` | Get one task |
| POST | `/tasks` | Create task |
| PUT | `/tasks/{id}` | Update task |
| DELETE | `/tasks/{id}` | Delete task |

## Required Status Codes

- GET success: 200
- POST success: 201
- DELETE success: 204
- Invalid request: 400
- Unknown task: 404

## Development Stages

### Stage 0 — Hello Server
Create the FastAPI application and verify localhost:8000.

### Stage 1 — Root and Health
Implement `/` and `/health`.

### Stage 2 — Read
Add in-memory tasks and GET endpoints.

### Stage 3 — Create
Add POST `/tasks` with validation.

### Stage 4 — Update/Delete
Complete CRUD.

### Stage 5 — Swagger
Document endpoints and verify `/docs`.

### Stage 6 — GitHub
Prepare README, screenshots and publish repository.

### Stage 7 — AI vs Me
Optional AI-generated implementation comparison.

## Agent Rules

Before modifying code:

1. Read this file.
2. Read README.md.
3. Inspect the current implementation.
4. Identify the current stage.
5. Do not redo completed stages unnecessarily.
6. Run tests after changes.
7. Update documentation when behavior changes.
8. Never claim a feature works without testing it.

## Current Stage

Stage 6 — Publish and docs.
