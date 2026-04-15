"""Session history formatting and basic aggregations."""

from collections import defaultdict
from datetime import date

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
