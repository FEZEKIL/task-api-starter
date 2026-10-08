# Architecture Documentation — Task API

## Overview

The **Task API** follows a clean, layered architecture incorporating the **Repository Pattern** for data storage and **Supabase Auth** for identity provider authentication and route protection.

```
                    ┌───────────────────────────┐
                    │       Supabase Auth       │
                    │   (Identity Provider)     │
                    └─────────────┬─────────────┘
                                  │
                       Issues / Verifies JWT
                                  │
                                  ▼
       ┌─────────────────────────────────────────────────┐
       │             HTTP Routes (app/main.py)           │
       │   Public Routes          Protected Routes       │
       │  (/public/info)   (Depends: get_current_user)  │
       └──────────────────────────┬──────────────────────┘
                                  │
                                  ▼
       ┌─────────────────────────────────────────────────┐
       │           Service Layer (app/services.py)       │
       └──────────────────────────┬──────────────────────┘
                                  │
                                  ▼
       ┌─────────────────────────────────────────────────┐
       │         Repository Abstraction (repo)          │
       └──────────────────────────┬──────────────────────┘
                                  │
         ┌────────────────────────┴────────────────────────┐
         ▼                                                 ▼
┌──────────────────┐                              ┌──────────────────┐
│ SQLite Repository│                              │ Postgres Repository
│(sqlite_repository)                              │(postgres_repository)
└──────────────────┘                              └──────────────────┘
```

## Architectural Rules

1. **Authentication & Authorization**:
   - Uses Supabase Auth as the external Identity Provider (IdP).
   - User credentials (email/password) are submitted to `POST /auth/signup` and `POST /auth/login`.
   - On successful authentication, Supabase returns a JSON Web Token (JWT) Access Token.
   - Protected routes (`/protected/profile`, `/protected/dashboard`, `/auth/logout`) use the FastAPI dependency `get_current_user`.
   - The dependency extracts the Bearer token from the `Authorization: Bearer <token>` HTTP header and verifies it via `supabase.auth.get_user(token)`.
   - Requests without a token or with an invalid/expired token immediately fail with HTTP 401 (`{"error": "Access token required"}` or `{"error": "Invalid or expired token"}`).

2. **Routes Layer (`app/main.py` / `app/auth.py`)**:
   - Manages HTTP status codes (200, 201, 204, 400, 401, 404).
   - Validates JSON body inputs and query parameters.
   - Delegates business operations directly to `TaskService` and authentication to Supabase Auth.

3. **Service Layer (`app/services.py`)**:
   - Orchestrates domain operations (`list_tasks`, `get_task`, `create_task`, `update_task`, `delete_task`, `get_stats`, `reset_tasks`).
   - Delegates persistence calls to `TaskRepository`.

4. **Repository Abstraction (`app/repository.py`)**:
   - Defines the abstract base class `TaskRepository`.
   - Specifies storage contract methods (`init_db`, `get_all`, `get_by_id`, `create`, `update`, `delete`, `get_stats`, `reset`).
   - Supports both `SQLiteTaskRepository` and `PostgresTaskRepository`.

## Security Trust Triangle

1. **Client**: Authenticates with email and password via `POST /auth/login`, receiving a JWT.
2. **Supabase IdP**: Validates credentials and generates signed JWT tokens.
3. **Backend Server**: Inspects incoming requests, parses the `Authorization` header, and verifies the JWT against Supabase before serving protected routes.
