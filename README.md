# Task API

A containerized CRUD REST API built with **Python**, **FastAPI**, **PostgreSQL**, and **Docker Compose** as part of the FlyRank Backend AI Engineering track (**BE-04: Containerize your stack**).

## Features

- Full task CRUD operations (Create, Read, Update, Delete)
- Storage abstraction using the **Repository Pattern**
- Dual storage support: **PostgreSQL** (containerized) and **SQLite** (local embedded)
- Fully containerized with **Docker** and **Docker Compose**
- Persistent storage using a named Docker volume (`postgres_data`)
- Health check and statistics endpoints (`/health`, `/stats`, `/reset`)
- Swagger / OpenAPI documentation (`/docs`)

## Tech Stack

- **Python 3.11+**
- **FastAPI**
- **Uvicorn**
- **PostgreSQL** & **`psycopg2-binary`**
- **Docker** & **Docker Compose**
- **SQLite** (for local/embedded mode)
- **pytest** & **httpx**

## Architecture & Storage Evolution

This project demonstrates clean architecture using the **Repository Pattern**:

```
In-memory repository ──► SQLite repository ──► PostgreSQL repository
```

### Key Architectural Guarantee

**Routes and service logic do NOT change when swapping storage implementations.**

- **Routes (`app/main.py`)**: Handle HTTP requests, responses, and input validation.
- **Service (`app/services.py`)**: Handles domain orchestration and business logic.
- **Repository Interface (`app/repository.py`)**: Abstract Base Class (`TaskRepository`) defining the storage contract.
- **Storage Implementations**:
  - `PostgresTaskRepository` (`app/postgres_repository.py`)
  - `SQLiteTaskRepository` (`app/repository.py`)

Changing storage implementations from SQLite to PostgreSQL only swaps the underlying repository implementation (`get_repository()`). Neither the route handlers nor the service functions contain any database-specific driver logic.

See [docs/architecture.md](docs/architecture.md) for detailed architecture documentation.

## Running with Docker Compose (Recommended)

Start the app and PostgreSQL database together with a single command:

```bash
docker-compose up --build
```

- **API URL**: http://localhost:8000
- **Interactive Swagger Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

To stop the containers:

```bash
docker-compose down
```

## Environment Configuration

Environment variables are managed using `.env`. A sample template is provided in `.env.example`:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=taskdb
POSTGRES_HOST=db
POSTGRES_PORT=5432
DATABASE_URL=postgresql://postgres:postgres@db:5432/taskdb
```

To run locally without Docker, create `.env` or set `DATABASE_URL=sqlite:///tasks.db`.

## Database & Initialization

- **Schema script**: `sql/init.sql` automatically runs when the PostgreSQL container starts for the first time.
- **Seed data**: Initial example tasks ("Buy groceries", "Read a book", "Write some code") are seeded automatically if the database table is empty.

### Example SQL Query (PostgreSQL)

Inspect the database inside the container:

```bash
docker-compose exec db psql -U postgres -d taskdb -c "SELECT * FROM tasks;"
```

## Proof of Persistence

Persistence across container and app restarts is guaranteed using a named Docker volume (`postgres_data`).

### Verification Steps

1. **Start the stack**:
   ```bash
   docker-compose up -d
   ```

2. **Create a new task**:
   ```bash
   curl -i -X POST http://localhost:8000/tasks \
     -H "Content-Type: application/json" \
     -d '{"title":"Persisted Task across restart"}'
   ```

3. **Restart the containers**:
   ```bash
   docker-compose restart
   ```

4. **Verify row persistence**:
   ```bash
   curl -i http://localhost:8000/tasks
   ```
   *Result*: The newly created task `"Persisted Task across restart"` is still present, proving data survives restarts.

## Endpoints

| Method | Endpoint | Status Codes | Description |
|---|---|---|---|
| GET | `/` | 200 | API Information |
| GET | `/health` | 200 | Health check |
| GET | `/tasks` | 200 | List tasks (supports `done` filter and `search`) |
| GET | `/tasks/{id}` | 200 / 404 | Get task by ID |
| POST | `/tasks` | 201 / 400 | Create task |
| PUT | `/tasks/{id}` | 200 / 400 / 404 | Update task title and/or done status |
| DELETE | `/tasks/{id}` | 204 / 404 | Delete task |
| GET | `/stats` | 200 | Task count statistics |
| POST | `/reset` | 200 | Reset tasks to default state |

## Running Tests

To run the automated test suite locally:

```bash
python -m pytest
```

## Project Documentation

- [docs/architecture.md](docs/architecture.md) — Architectural pattern and storage abstraction breakdown
- [docs/stages.md](docs/stages.md) — Progress tracking across BE-01, BE-02, and BE-04
- [Agent.md](Agent.md) — Agent instructions and constraint rules
