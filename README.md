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
- In-memory storage

## Tech Stack

- Python
- FastAPI
- Uvicorn
- pytest

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

- **Filtering**: `GET /tasks?done=true` or `GET /tasks?done=false`
- **Search**: `GET /tasks?search=milk`
- **Stats**: `GET /stats` returns a summary of tasks.
- **Reset**: `POST /reset` restores the initial 3 example tasks.

## Example Usage

### Get all tasks
```bash
curl -i http://localhost:8000/tasks
```
Output:
```
HTTP/1.1 200 OK
content-length: 154
content-type: application/json

[{"id":1,"title":"Buy groceries","done":false},{"id":2,"title":"Read a book","done":true},{"id":3,"title":"Write some code","done":false}]
```

### Create a task
```bash
curl -i -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d '{"title":"Buy milk"}'
```
Output:
```
HTTP/1.1 201 Created
content-length: 44
content-type: application/json

{"id":4,"title":"Buy milk","done":false}
```

## Swagger UI Screenshot

![Swagger UI](screenshots/swagger.png)
*(Note: Replace this placeholder with an actual screenshot from your local /docs page)*

## Project Stages

See docs/stages.md.

## AI Development

See Agent.md.

The optional AI comparison is documented in ai-version/.
