import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv("SQLITE_DB_PATH", "tasks.db")
DATABASE_URL = os.getenv("DATABASE_URL", "")

def get_db_type() -> str:
    db_type = os.getenv("DB_TYPE", "").lower()
    if db_type in ("postgres", "postgresql"):
        return "postgres"
    if DATABASE_URL.startswith("postgresql://") or DATABASE_URL.startswith("postgres://"):
        return "postgres"
    return "sqlite"

def get_sqlite_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_postgres_connection():
    import psycopg2
    from psycopg2.extras import RealDictCursor

    url = DATABASE_URL
    if not url or url.startswith("sqlite"):
        host = os.getenv("POSTGRES_HOST", "localhost")
        port = os.getenv("POSTGRES_PORT", "5432")
        user = os.getenv("POSTGRES_USER", "postgres")
        password = os.getenv("POSTGRES_PASSWORD", "postgres")
        dbname = os.getenv("POSTGRES_DB", "taskdb")
        url = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"

    conn = psycopg2.connect(url, cursor_factory=RealDictCursor)
    return conn
