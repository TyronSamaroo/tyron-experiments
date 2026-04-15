"""Session history formatting, streak tracking, and daily summary."""

from collections import defaultdict
from datetime import date, timedelta

from colorama import Fore, Style, init as colorama_init

from pomodoro.db import Session

colorama_init(autoreset=True)

TYPE_COLORS = {
    "work": Fore.RED,
    "short_break": Fore.GREEN,
    "long_break": Fore.CYAN,
}


def _colorize_type(session_type: str) -> str:
    color = TYPE_COLORS.get(session_type, Fore.WHITE)
    label = session_type.replace("_", " ").title()
    return f"{color}{Style.BRIGHT}{label}{Style.RESET_ALL}"


def format_history_table(sessions: list[Session]) -> str:
    """Return a colorized table of recent sessions."""
    if not sessions:
        return f"{Fore.YELLOW}No sessions recorded yet. Run `pomodoro start` to begin!{Style.RESET_ALL}"

    header = (
        f"{Style.BRIGHT}"
        f"{'#':<5} {'Type':<22} {'Date':<12} {'Started':<10} {'Duration':>9} {'Done':>5}"
        f"{Style.RESET_ALL}"
    )
    divider = "-" * 58
    rows = [header, divider]

    for s in sessions:
        started = s.started_at[:19]
        d = started[:10]
        t = started[11:16]
        done_str = f"{Fore.GREEN}yes{Style.RESET_ALL}" if s.completed else f"{Fore.RED}no{Style.RESET_ALL}"
        type_col = _colorize_type(s.session_type)
        rows.append(
            f"{s.id:<5} {type_col:<30} {d:<12} {t:<10} {s.duration_minutes:>6} min {done_str:>5}"
        )

    return "\n".join(rows)


def total_work_minutes(sessions: list[Session]) -> int:
    return sum(s.duration_minutes for s in sessions if s.session_type == "work" and s.completed)


def sessions_by_day(sessions: list[Session]) -> dict[date, list[Session]]:
    result: dict[date, list[Session]] = defaultdict(list)
    for s in sessions:
        day = date.fromisoformat(s.started_at[:10])
        result[day].append(s)
    return result


def current_streak(sessions: list[Session]) -> int:
    """
    Return the number of consecutive calendar days (ending today or yesterday)
    on which at least one completed work session was logged.
    """
    days_with_work = {
        date.fromisoformat(s.started_at[:10])
        for s in sessions
        if s.session_type == "work" and s.completed
    }
    if not days_with_work:
        return 0

    today = date.today()
    # Allow streak to carry over if no session yet today
    check = today if today in days_with_work else today - timedelta(days=1)
    streak = 0
    while check in days_with_work:
        streak += 1
        check -= timedelta(days=1)
    return streak


def daily_summary(sessions: list[Session], target_date: date | None = None) -> str:
    """Return a one-line summary for a given date (defaults to today)."""
    target_date = target_date or date.today()
    by_day = sessions_by_day(sessions)
    day_sessions = by_day.get(target_date, [])

    completed_work = [s for s in day_sessions if s.session_type == "work" and s.completed]
    total_mins = sum(s.duration_minutes for s in completed_work)
    hours, mins = divmod(total_mins, 60)

    date_str = target_date.strftime("%b %d, %Y")
    pomodoros = len(completed_work)

    if not completed_work:
        return (
            f"{Fore.YELLOW}{date_str}: no completed work sessions yet.{Style.RESET_ALL}"
        )

    return (
        f"{Fore.GREEN}{Style.BRIGHT}{date_str}:{Style.RESET_ALL} "
        f"{Fore.RED}{pomodoros} Pomodoro{'s' if pomodoros != 1 else ''}{Style.RESET_ALL} "
        f"— {hours}h {mins}m of focused work"
    )
