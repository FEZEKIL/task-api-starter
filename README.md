# Task API

A containerized CRUD REST API with **Supabase JWT Authentication**, built with **Python**, **FastAPI**, **PostgreSQL**, and **Docker Compose** as part of the FlyRank Backend AI Engineering track (**BE-03: Auth - Login & Protect** and **BE-04: Containerize your stack**).

## Features

- **Authentication & Authorization**:
  - Sign Up (`POST /auth/signup`)
  - Log In (`POST /auth/login`) with JWT token issuance
  - Log Out (`POST /auth/logout`)
  - Protected endpoints (`GET /protected/profile`, `GET /protected/dashboard`) using FastAPI dependency token verification
  - Public info endpoint (`GET /public/info`)
- **Task CRUD operations**:
  - Create, Read, Update, Delete tasks with filtering and statistics (`/tasks`, `/stats`, `/reset`)
- **Storage Abstraction**:
  - Repository Pattern supporting containerized **PostgreSQL** and local **SQLite**
- **Containerization**:
  - Fully containerized with **Docker** and **Docker Compose**
  - Persistent database storage volume (`postgres_data`)
- **Swagger / OpenAPI Documentation**:
  - Interactive Swagger UI at `/docs` with `HTTPBearer` authorization padlock

## Tech Stack

- **Python 3.11+**
- **FastAPI**
- **Supabase Python SDK (`supabase`)**
- **Uvicorn**
- **PostgreSQL** & **`psycopg2-binary`**
- **Docker** & **Docker Compose**
- **SQLite**
- **pytest** & **httpx**

## Authentication Architecture

Authentication is managed via Supabase Auth as the Identity Provider (IdP):

```
Client ──► POST /auth/login (email, password) ──► Supabase Auth ──► Returns JWT
Client ──► GET /protected/profile (Authorization: Bearer <JWT>) ──► FastAPI Backend ──► Verifies Token ──► Returns Profile (200)
```

### Protected Endpoint Rules

Protected endpoints require the client to supply their access token in the request header:

```http
Authorization: Bearer <access_token>
```

- **Missing header**: Returns HTTP `401 Unauthorized` with `{"error": "Access token required"}`
- **Invalid / Expired token**: Returns HTTP `401 Unauthorized` with `{"error": "Invalid or expired token"}`
- **Valid token**: Returns HTTP `200 OK` with user data.

## Running the API

### Option 1: Docker Compose (Recommended)

Start the API and PostgreSQL container together:

```bash
docker-compose up --build
```

- **API Base URL**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Option 2: Local Python Execution

1. Create a virtual environment and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure `.env` (copy from `.env.example`):
   ```bash
   cp .env.example .env
   ```
3. Run the API with Uvicorn:
   ```bash
   uvicorn app.main:app --reload
   ```

## Environment Configuration

Secrets and configuration parameters are loaded from `.env` (gitignored, template in `.env.example`):

```env
# Database configuration
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=taskdb
POSTGRES_HOST=db
POSTGRES_PORT=5432
DATABASE_URL=postgresql://postgres:postgres@db:5432/taskdb

# Supabase Auth configuration
SUPABASE_URL=https://your-project-url.supabase.co
SUPABASE_KEY=your-anon-key
```

## API Endpoints Reference

| Method | Endpoint | Auth Required | Status Codes | Purpose |
|---|---|---|---|---|
| GET | `/` | No | 200 | API Information |
| GET | `/health` | No | 200 | Health check |
| GET | `/public/info` | No | 200 | Public info endpoint |
| POST | `/auth/signup` | No | 201 / 400 | Sign up a new user |
| POST | `/auth/login` | No | 200 / 400 / 401 | Authenticate user & return JWT |
| POST | `/auth/logout` | Yes (Bearer) | 204 / 401 | Terminate user session |
| GET | `/protected/profile` | Yes (Bearer) | 200 / 401 | Read private user profile |
| GET | `/protected/dashboard` | Yes (Bearer) | 200 / 401 | Read protected user dashboard |
| GET | `/tasks` | No | 200 | List tasks |
| GET | `/tasks/{id}` | No | 200 / 404 | Get single task |
| POST | `/tasks` | No | 201 / 400 | Create task |
| PUT | `/tasks/{id}` | No | 200 / 400 / 404 | Update task |
| DELETE | `/tasks/{id}` | No | 204 / 404 | Delete task |
| GET | `/stats` | No | 200 | Get task statistics |
| POST | `/reset` | No | 200 | Reset tasks database |

## Example cURL Commands

### 1. Sign Up
```bash
curl -i -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com", "password":"password123"}'
```

### 2. Log In
```bash
curl -i -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com", "password":"password123"}'
```

### 3. Access Protected Profile
```bash
curl -i http://localhost:8000/protected/profile \
  -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>"
```

### 4. Log Out
```bash
curl -i -X POST http://localhost:8000/auth/logout \
  -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>"
```

## Running Tests

Run the complete test suite (21 tests covering tasks, repositories, and auth):

```bash
python -m pytest
```

## Documentation

- [docs/architecture.md](docs/architecture.md) — Architecture & security trust triangle
- [docs/stages.md](docs/stages.md) — Stage progress across BE-01, BE-02, BE-04, and BE-03
- [Agent.md](Agent.md) — Agent constraints and instructions
