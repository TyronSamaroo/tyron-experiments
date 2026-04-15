"""Entry point for the pomodoro CLI."""

from datetime import datetime

import click
from colorama import Fore, Style

from pomodoro.config import load_config, save_config, reset_config
from pomodoro.db import save_session, fetch_sessions, fetch_all_sessions
from pomodoro.stats import format_history_table, total_work_minutes
from pomodoro.timer import countdown, SessionType

LABELS = {
    SessionType.WORK: "Work",
    SessionType.SHORT_BREAK: "Short Break",
    SessionType.LONG_BREAK: "Long Break",
}


def _durations_from_config() -> dict[SessionType, int]:
    cfg = load_config()
    return {
        SessionType.WORK: cfg["work_minutes"],
        SessionType.SHORT_BREAK: cfg["short_break_minutes"],
        SessionType.LONG_BREAK: cfg["long_break_minutes"],
    }


@click.group()
def main():
    """Pomodoro CLI — stay focused, track your sessions."""
    pass


@main.command()
@click.option("--short", "session_type", flag_value="short_break", help="Short break (default 5 min)")
@click.option("--long", "session_type", flag_value="long_break", help="Long break (default 15 min)")
@click.option("--work", "session_type", flag_value="work", default=True, help="Work session (default 25 min)")
def start(session_type: str):
    """Start a Pomodoro session (work, short break, or long break)."""
    stype = SessionType(session_type)
    durations = _durations_from_config()
    minutes = durations[stype]
    label = LABELS[stype]

    click.echo(f"Starting {minutes}-min {label} session. Press Ctrl+C to cancel.\n")
    started_at = datetime.now()
    completed = countdown(minutes * 60, label=label)
    ended_at = datetime.now()

    save_session(
        session_type=stype.value,
        started_at=started_at,
        ended_at=ended_at,
        completed=completed,
        duration_minutes=minutes,
    )

    if completed:
        messages = {
            SessionType.WORK: "Great work! Time for a break.",
            SessionType.SHORT_BREAK: "Break over — back to it!",
            SessionType.LONG_BREAK: "Refreshed? Let's get back to work.",
        }
        click.echo(messages[stype])
    else:
        click.echo("Session cancelled — saved as incomplete.")


@main.command()
@click.option("--limit", default=20, show_default=True, help="Number of recent sessions to show")
def stats(limit: int):
    """Show session history and total focused time."""
    sessions = fetch_sessions(limit=limit)
    all_sessions = fetch_all_sessions()

    click.echo("\n--- Recent Sessions ---\n")
    click.echo(format_history_table(sessions))

    total = total_work_minutes(all_sessions)
    hours, mins = divmod(total, 60)
    click.echo(f"\nTotal focused time (all time): {hours}h {mins}m across {len(all_sessions)} sessions.\n")


@main.command("config")
@click.option("--work", "work_minutes", type=int, default=None, help="Work session duration in minutes")
@click.option("--short", "short_minutes", type=int, default=None, help="Short break duration in minutes")
@click.option("--long", "long_minutes", type=int, default=None, help="Long break duration in minutes")
@click.option("--reset", is_flag=True, help="Reset all durations to defaults")
def config_cmd(work_minutes, short_minutes, long_minutes, reset):
    """Show or update timer durations."""
    if reset:
        reset_config()
        click.echo("Config reset to defaults.")

    if any(v is not None for v in (work_minutes, short_minutes, long_minutes)):
        cfg = load_config()
        if work_minutes is not None:
            cfg["work_minutes"] = work_minutes
        if short_minutes is not None:
            cfg["short_break_minutes"] = short_minutes
        if long_minutes is not None:
            cfg["long_break_minutes"] = long_minutes
        save_config(cfg)
        click.echo("Config updated.")

    cfg = load_config()
    click.echo(
        f"\n{Style.BRIGHT}Current durations:{Style.RESET_ALL}\n"
        f"  {Fore.RED}Work        {cfg['work_minutes']} min{Style.RESET_ALL}\n"
        f"  {Fore.GREEN}Short break {cfg['short_break_minutes']} min{Style.RESET_ALL}\n"
        f"  {Fore.CYAN}Long break  {cfg['long_break_minutes']} min{Style.RESET_ALL}\n"
    )


if __name__ == "__main__":
    main()
