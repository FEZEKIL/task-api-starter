# Development Stages

## BE-01 — In-Memory CRUD
- [x] Stage 0 — Hello server
- [x] Stage 1 — Root and health endpoints
- [x] Stage 2 — Read endpoints
- [x] Stage 3 — Create endpoint
- [x] Stage 4 — Update and delete
- [x] Stage 5 — Swagger UI
- [x] Stage 6 — GitHub publication

## BE-02 — Database Persistence
- [x] Stage 0 — Create SQLite database
- [x] Stage 1 — Read from database
- [x] Stage 2 — Create new tasks
- [x] Stage 3 — Update and delete with SQL
- [x] Stage 4 — Explore SQLite
- [x] Stage 5 — Database documentation

## BE-04 — Containerize your stack
- [x] Stage 0 — Docker / Postgres setup (`Dockerfile`, `docker-compose.yml`)
- [x] Stage 1 — Environment configuration (`.env`, `.env.example`)
- [x] Stage 2 — Database schema (`sql/init.sql`)
- [x] Stage 3 — PostgreSQL repository (`app/postgres_repository.py`)
- [x] Stage 4 — Repository swap & abstraction (`app/repository.py`, `app/services.py`)
- [x] Stage 5 — Docker Compose stack
- [x] Stage 6 — Persistence verification
- [x] Stage 7 — Stack documentation

## BE-03 — Auth - Login & Protect
- [x] Stage 0 — Setup Supabase & Server (`SUPABASE_URL`, `SUPABASE_KEY` client initialization)
- [x] Stage 1 — Open Auth: Sign Up (`POST /auth/signup`) & Log In (`POST /auth/login`)
- [x] Stage 2 — Public & Protected Gates (`GET /public/info` & unverified/protected profile structure)
- [x] Stage 3 — The Guard: Token Verification (`GET /protected/profile` verifying JWT with Supabase)
- [x] Stage 4 — Dependency Protection & Logout (`get_current_user`, `POST /auth/logout`, `GET /protected/dashboard`)
- [x] Stage 5 — Swagger UI Authorization (`HTTPBearer` scheme with padlock at `/docs`)
- [x] Stage 6 — Documentation & GitHub publication

## A9 — The Polite Scraper
- [x] Stage 0 — Classify scraping target (`https://books.toscrape.com`, `robots.txt` check, policy statement)
- [x] Stage 1 — Fetch and cache HTML (`PoliteFetcher`, User-Agent, timeout, disk caching)
- [x] Stage 2 — Discover three catalogue pages (extract product URLs, follow next link, 500ms delay, deduplicate)
- [x] Stage 3 — Extract book details (parse 60 detail pages, extract 8 raw fields + provenance)
- [x] Stage 4 — Validate normalized records (`price_gbp` float, Pydantic schema validation, `output/books.json`)
- [x] Stage 5 — Survive failures and report the run (exception boundaries, 1 retry for 5xx/timeouts, `output/run-report.json`, test with broken URL)
- [x] Stage 6 — Publish scraper evidence (`scraper/README.md`, schema, run metrics, no-browser justification, ethics statement)

## Stage Completion Rules

A stage is only considered complete when:

1. Implementation exists.
2. Endpoint has been tested (if applicable).
3. Expected status code has been verified.
4. Documentation has been updated.
5. Git commit has been created.
