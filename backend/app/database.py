import sqlite3
from datetime import UTC, datetime
from typing import Any

from app.config import DB_PATH


def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # Enable WAL mode per docs/06-architecture.md
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn


def init_db() -> None:
    conn = get_db_connection()
    try:
        with conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS health_status (
                    id INTEGER PRIMARY KEY,
                    status_key TEXT UNIQUE NOT NULL,
                    status_value TEXT NOT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            )
            conn.execute(
                """
                INSERT INTO health_status (id, status_key, status_value)
                VALUES (1, 'system_health', 'SQLite WAL Connected and Healthy')
                ON CONFLICT(id) DO UPDATE SET
                    status_value='SQLite WAL Connected and Healthy',
                    updated_at=CURRENT_TIMESTAMP;
                """
            )
    finally:
        conn.close()


def read_db_health_value() -> dict[str, Any]:
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT status_value, updated_at FROM health_status WHERE id = 1;"
        )
        row = cursor.fetchone()
        journal_mode_row = conn.execute("PRAGMA journal_mode;").fetchone()
        mode = journal_mode_row[0] if journal_mode_row else "WAL"

        if row:
            value = str(row["status_value"])
            timestamp = row["updated_at"]
        else:
            value = "SQLite Initialized"
            timestamp = datetime.now(UTC).isoformat()

        return {
            "status": "connected",
            "mode": mode.upper(),
            "value": value,
            "timestamp": timestamp,
        }
    except Exception as exc:
        return {
            "status": "error",
            "mode": "UNKNOWN",
            "value": f"DB Error: {exc}",
            "timestamp": datetime.now(UTC).isoformat(),
        }
    finally:
        conn.close()
