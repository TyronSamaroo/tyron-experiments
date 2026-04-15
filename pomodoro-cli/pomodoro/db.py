"""SQLite session storage."""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import NamedTuple

DB_PATH = Path.home() / ".pomodoro_sessions.db"


class Session(NamedTuple):
    id: int
    session_type: str
    started_at: str
    ended_at: str
    completed: bool
    duration_minutes: int


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create the sessions table if it does not exist."""
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS sessions (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                session_type    TEXT NOT NULL,
                started_at      TEXT NOT NULL,
                ended_at        TEXT NOT NULL,
                completed       INTEGER NOT NULL DEFAULT 1,
                duration_minutes INTEGER NOT NULL
            )
            """
        )


def save_session(
    session_type: str,
    started_at: datetime,
    ended_at: datetime,
    completed: bool,
    duration_minutes: int,
) -> int:
    """Persist a session and return its new id."""
    init_db()
    with _connect() as conn:
        cursor = conn.execute(
            """
            INSERT INTO sessions (session_type, started_at, ended_at, completed, duration_minutes)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                session_type,
                started_at.isoformat(),
                ended_at.isoformat(),
                int(completed),
                duration_minutes,
            ),
        )
        return cursor.lastrowid


def fetch_sessions(limit: int = 20) -> list[Session]:
    """Return the most recent sessions, newest first."""
    init_db()
    with _connect() as conn:
        rows = conn.execute(
            """
            SELECT id, session_type, started_at, ended_at, completed, duration_minutes
            FROM sessions
            ORDER BY started_at DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    return [Session(*row) for row in rows]


def fetch_all_sessions() -> list[Session]:
    """Return all sessions for stats calculations."""
    init_db()
    with _connect() as conn:
        rows = conn.execute(
            """
            SELECT id, session_type, started_at, ended_at, completed, duration_minutes
            FROM sessions
            ORDER BY started_at ASC
            """
        ).fetchall()
    return [Session(*row) for row in rows]
