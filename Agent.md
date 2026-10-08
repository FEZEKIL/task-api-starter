# Agent Instructions

## Project

Task API — FlyRank Backend AI Engineering (Containerized PostgreSQL & Supabase Auth Stack).

This repository implements a CRUD REST API built with FastAPI, supporting storage abstraction via the Repository Pattern (SQLite and PostgreSQL options) and full user authentication via Supabase Auth (Sign Up, Log In, Log Out, and Protected Routes).

## Primary Goal

Provide a secure containerized application featuring Supabase JWT authentication, protected endpoints, and a PostgreSQL database abstraction while preserving existing routes and contracts.

## Technology

- Python 3.11+
- FastAPI
- Supabase Python SDK (`supabase`)
- Uvicorn
- pytest
- PostgreSQL & psycopg2-binary
- SQLite & sqlite3
- Docker & Docker Compose
- Swagger/OpenAPI via FastAPI

## Important Constraints

1. Supabase Auth parameters (`SUPABASE_URL`, `SUPABASE_KEY`) and database credentials are loaded from `.env` (`.env.example` committed).
2. Data persists across container restarts using named Docker volume `postgres_data`.
3. Initial schema and seed data are populated via `sql/init.sql`.
4. **Architectural Rule**: Routes and service logic MUST NOT contain database-specific logic. Repository layer abstracts storage.
5. **Auth Rule**: Token verification is enforced via reusable FastAPI Dependency (`get_current_user`). Protected endpoints require `Authorization: Bearer <token>`.
6. Swagger UI remains available at `/docs` with interactive `HTTPBearer` authorization padlock.

## BE-03 Auth Status

- Stage 0 — Setup Supabase & Server (`SUPABASE_URL`, `SUPABASE_KEY`)
- Stage 1 — Open Auth: Sign Up (`POST /auth/signup`) & Log In (`POST /auth/login`)
- Stage 2 — Public & Protected Gates (`GET /public/info` & profile route)
- Stage 3 — Token Verification (`GET /protected/profile` via `supabase.auth.get_user()`)
- Stage 4 — Reusable Dependency (`get_current_user`), Logout (`POST /auth/logout`), & Dashboard (`GET /protected/dashboard`)
- Stage 5 — Swagger UI Authorization (`HTTPBearer` scheme)
- Stage 6 — Documentation & GitHub publication

## Required Endpoints

| Method | Endpoint | Purpose | Authorization |
|---|---|---|---|
| GET | `/` | API information | None |
| GET | `/health` | Health check | None |
| GET | `/public/info` | Public info | None |
| POST | `/auth/signup` | Sign Up | None |
| POST | `/auth/login` | Log In & JWT Issue | None |
| POST | `/auth/logout` | Log Out / Terminate session | Bearer JWT |
| GET | `/protected/profile` | Read user profile | Bearer JWT |
| GET | `/protected/dashboard` | Read user dashboard | Bearer JWT |
| GET | `/tasks` | List tasks | None |
| GET | `/tasks/{id}` | Get one task | None |
| POST | `/tasks` | Create task | None |
| PUT | `/tasks/{id}` | Update task | None |
| DELETE | `/tasks/{id}` | Delete task | None |
| GET | `/stats` | Task statistics | None |
| POST | `/reset` | Reset database tasks | None |

## Required Status Codes

- GET success: 200
- POST signup success: 201
- POST login success: 200
- POST logout / DELETE success: 204
- Invalid input / missing fields: 400
- Unauthorized / missing / invalid token / bad credentials: 401
- Unknown task / resource: 404

## Agent Rules

Before modifying code:

1. Read this file.
2. Read README.md and docs/architecture.md.
3. Do not violate repository abstraction or authentication boundaries.
4. Run tests (`python -m pytest`) after changes.
5. Never claim a feature works without verifying tests.

## Current Stage

BE-03 Auth & BE-04 Containerized Stack — Completed.
