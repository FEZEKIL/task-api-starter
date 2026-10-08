# Agent Instructions

## Project

Task API — FlyRank Backend AI Engineering BE-04 (Containerized PostgreSQL Stack).

This repository implements a CRUD REST API built with FastAPI, supporting storage abstraction via the Repository Pattern with both embedded SQLite and containerized PostgreSQL storage options.

## Primary Goal

Containerize the FastAPI application and PostgreSQL database with Docker Compose, implementing a PostgreSQL repository abstraction while preserving existing routes and business service logic unchanged.

## Technology

- Python 3.10+
- FastAPI
- Uvicorn
- pytest
- PostgreSQL
- psycopg2-binary
- SQLite & sqlite3
- Docker & Docker Compose
- Swagger/OpenAPI via FastAPI

## Important Constraints

1. Application and database run together via `docker compose up`.
2. PostgreSQL database credentials and connection parameters are loaded from `.env` (gitignored, `.env.example` committed).
3. Data persists across container restarts using named Docker volume `postgres_data`.
4. Initial schema and seed data are populated via `sql/init.sql`.
5. **Architectural Rule**: Routes and service logic MUST NOT contain database-specific logic. Changing storage implementations from SQLite to PostgreSQL only swaps the repository layer implementation.
6. All required HTTP status codes and API contracts remain identical to BE-01 and BE-02.
7. Validation errors must return JSON containing `error`.
8. Swagger UI remains available at `/docs`.

## BE-04 STATUS

- Stage 0 — Docker/Postgres setup (`Dockerfile`, `docker-compose.yml`)
- Stage 1 — Environment configuration (`.env`, `.env.example`)
- Stage 2 — Database schema (`sql/init.sql`)
- Stage 3 — PostgreSQL repository (`app/postgres_repository.py`)
- Stage 4 — Repository swap & layer separation (`app/repository.py`, `app/services.py`)
- Stage 5 — Docker Compose stack
- Stage 6 — Persistence verification
- Stage 7 — Documentation (`README.md`, `Agent.md`, `docs/architecture.md`, `docs/stages.md`)

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
| GET | `/stats` | Task statistics |
| POST | `/reset` | Reset database tasks |

## Required Status Codes

- GET success: 200
- POST success: 201
- DELETE success: 204
- Invalid request: 400
- Unknown task: 404

## Agent Rules

Before modifying code:

1. Read this file.
2. Read README.md and docs/architecture.md.
3. Inspect current repository implementation.
4. Do not violate repository abstraction boundaries.
5. Run tests (`python -m pytest`) after changes.
6. Never claim a feature works without verifying tests.

## Current Stage

BE-04 Containerized Stack — Completed.
