# Agent Instructions

## Project

Task API — FlyRank Backend AI Engineering BE-02.

This repository implements a small CRUD API using Python and FastAPI, now backed by a SQLite database.

## Primary Goal

Replace the in-memory storage with a persistent SQLite database while maintaining the same API contract.

## Technology

- Python 3.10+
- FastAPI
- Uvicorn
- pytest
- SQLite
- sqlite3 (Python standard library)
- Swagger/OpenAPI via FastAPI

## Important Constraints

1. Tasks must be stored in a SQLite database (`tasks.db`).
2. Data must survive server restarts.
3. The database and table must be created automatically if they don't exist.
4. Three example tasks must be inserted only if the table is empty.
5. Required endpoints must remain available and behave identically to BE-01.
6. Required HTTP status codes must not be changed.
7. Validation errors must return JSON containing `error`.
8. Swagger UI must remain available at `/docs`.
9. `tasks.db` must NOT be committed to Git.

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

## Development Stages (BE-02)

### Stage 0 — Create SQLite database
Create `tasks.db` and the `tasks` table. Insert example tasks if empty.

### Stage 1 — Read from database
Replace in-memory read logic with SQL queries.

### Stage 2 — Create new tasks
Replace in-memory creation with SQL `INSERT`.

### Stage 3 — Update and delete with SQL
Replace in-memory update/delete with SQL `UPDATE` and `DELETE`.

### Stage 4 — Explore SQLite
Verify manual SQL queries and API reflection.

### Stage 5 — Database Documentation
Update README with SQLite details and database screenshots.

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

BE-02 Stage 0 — Create SQLite database.
