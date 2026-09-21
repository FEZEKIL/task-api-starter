# Task API

A small CRUD REST API built with Python and FastAPI as part of the
FlyRank Backend AI Engineering internship.

## Features

- Create tasks
- Read tasks
- Update tasks
- Delete tasks
- Health check
- Swagger/OpenAPI documentation
- **Persistent storage with SQLite**

## Tech Stack

- Python
- FastAPI
- Uvicorn
- pytest
- **SQLite**

## Database

This project uses **SQLite** for data persistence. 

- **Why SQLite?** It's lightweight, serverless, and stores the entire database in a single file (`tasks.db`). This makes it perfect for development and small applications without needing a complex database server setup.
- **Storage**: The database is stored in `tasks.db` in the project root. This file is automatically created and initialized with example tasks on the first run.

### Example SQL Query
You can inspect the database using any SQLite viewer. Here is an example query to list all tasks:
```sql
SELECT * FROM tasks;
```

## Run Locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API: http://localhost:8000
Swagger: http://localhost:8000/docs

## Endpoints

| Method | Endpoint | Status |
|---|---|---|
| GET | / | 200 |
| GET | /health | 200 |
| GET | /tasks | 200 |
| GET | /tasks/{id} | 200 / 404 |
| POST | /tasks | 201 / 400 |
| PUT | /tasks/{id} | 200 / 400 / 404 |
| DELETE | /tasks/{id} | 204 / 404 |
| GET | /stats | 200 |
| POST | /reset | 200 |

## Extras

- **Filtering**: `GET /tasks?done=true` or `GET /tasks?done=false` (using SQL `WHERE`)
- **Search**: `GET /tasks?search=milk` (using SQL `LIKE`)
- **Stats**: `GET /stats` (using SQL `COUNT()`)
- **Reset**: `POST /reset` (clears and restores initial tasks)

## Example Usage

### Get all tasks
```bash
curl -i http://localhost:8000/tasks
```

### Create a task
```bash
curl -i -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d '{"title":"Buy milk"}'
```

## Swagger UI Screenshot

![Swagger UI](screenshots/swagger.png)

## Database Viewer Screenshot

![Database Viewer](screenshots/database.png)
*(Note: Replace this placeholder with a screenshot of your DB Browser for SQLite showing the tasks table)*

## Project Stages

See docs/stages.md.

## AI Development

See Agent.md.

The optional AI comparison is documented in ai-version/.
