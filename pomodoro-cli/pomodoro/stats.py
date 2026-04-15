"""Session history formatting and basic aggregations."""

from collections import defaultdict
from datetime import date

from pomodoro.db import fetch_sessions, fetch_all_sessions, Session


def format_history_table(sessions: list[Session]) -> str:
    """Return a plain-text table of recent sessions."""
    if not sessions:
        return "No sessions recorded yet. Run `pomodoro start` to begin!"

    header = f"{'#':<5} {'Type':<14} {'Date':<12} {'Started':<10} {'Duration':>9} {'Done':>5}"
    divider = "-" * len(header)
    rows = [header, divider]

    for s in sessions:
        started = s.started_at[:19]  # ISO up to seconds
        d = started[:10]
        t = started[11:16]
        done = "yes" if s.completed else "no"
        type_label = s.session_type.replace("_", " ").title()
        rows.append(f"{s.id:<5} {type_label:<14} {d:<12} {t:<10} {s.duration_minutes:>6} min {done:>5}")

    return "\n".join(rows)


def total_work_minutes(sessions: list[Session]) -> int:
    return sum(s.duration_minutes for s in sessions if s.session_type == "work" and s.completed)


def sessions_by_day(sessions: list[Session]) -> dict[date, list[Session]]:
    result: dict[date, list[Session]] = defaultdict(list)
    for s in sessions:
        day = date.fromisoformat(s.started_at[:10])
        result[day].append(s)
    return result
