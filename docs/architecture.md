# Architecture Documentation — Task API

## Overview

The **Task API** follows a clean, layered architecture implementing the **Repository Pattern**. This pattern decouples business logic and HTTP routing from the underlying data persistence mechanism.

```
       ┌───────────────────────────────┐
       │   HTTP Routes (app/main.py)   │
       └──────────────┬────────────────┘
                      │
                      ▼
       ┌───────────────────────────────┐
       │   Service Layer (services.py) │
       └──────────────┬────────────────┘
                      │
                      ▼
       ┌───────────────────────────────┐
       │ Repository Abstraction (repo) │
       └──────────────┬────────────────┘
                      │
         ┌────────────┴────────────┐
         ▼                         ▼
┌──────────────────┐      ┌──────────────────┐
│  SQLite Repository│      │PostgreSQL Repository
│(sqlite_repository)│     │(postgres_repository)
└──────────────────┘      └──────────────────┘
```

## Architectural Rules

1. **Routes Layer (`app/main.py`)**:
   - Manages HTTP status codes (200, 201, 204, 400, 404).
   - Validates JSON body inputs and query parameters.
   - Delegates business operations directly to `TaskService`.
   - **Contains zero database-specific code**.

2. **Service Layer (`app/services.py`)**:
   - Orchestrates domain operations (`list_tasks`, `get_task`, `create_task`, `update_task`, `delete_task`, `get_stats`, `reset_tasks`).
   - Translates domain models to dict representations.
   - Delegates persistence calls to `TaskRepository`.
   - **Contains zero database-specific SQL or driver logic**.

3. **Repository Abstraction (`app/repository.py`)**:
   - Defines the abstract base class `TaskRepository`.
   - Specifies contract methods:
     - `init_db()`
     - `get_all(done, search)`
     - `get_by_id(task_id)`
     - `create(title)`
     - `update(task_id, title, done)`
     - `delete(task_id)`
     - `get_stats()`
     - `reset()`

4. **Repository Implementations**:
   - **`SQLiteTaskRepository`**: Embedded file-based storage using Python's standard `sqlite3` module.
   - **`PostgresTaskRepository`**: Containerized database storage using `psycopg2-binary`.

5. **Storage Swapping**:
   - The factory function `get_repository()` evaluates the environment variable `DATABASE_URL` or `DB_TYPE`.
   - When running locally, it defaults to SQLite.
   - When running in Docker Compose (`DB_TYPE=postgres` or `DATABASE_URL=postgresql://...`), it seamlessly instantiates `PostgresTaskRepository`.
   - **Swapping databases requires zero changes to routes or service code.**

## Persistence Proof Procedure

1. Start the stack: `docker compose up -d`
2. Create a task via HTTP request:
   `curl -i -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d '{"title":"Persisted Task"}'`
3. Restart app and database containers: `docker compose restart`
4. Fetch tasks to verify row persistence:
   `curl -i http://localhost:8000/tasks`
5. The row with `"title": "Persisted Task"` remains present in PostgreSQL storage volume `postgres_data`.
