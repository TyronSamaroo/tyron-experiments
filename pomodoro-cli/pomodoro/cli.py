"""Entry point for the pomodoro CLI."""

from datetime import datetime

import click
from pomodoro.db import save_session
from pomodoro.timer import countdown, SessionType

DEFAULT_DURATIONS = {
    SessionType.WORK: 25,
    SessionType.SHORT_BREAK: 5,
    SessionType.LONG_BREAK: 15,
}


@click.group()
def main():
    """Pomodoro CLI — stay focused, track your sessions."""
    pass


@main.command()
@click.option("--short", "session_type", flag_value="short_break", help="5-min short break")
@click.option("--long", "session_type", flag_value="long_break", help="15-min long break")
@click.option("--work", "session_type", flag_value="work", default=True, help="25-min work session (default)")
def start(session_type: str):
    """Start a Pomodoro session (work, short break, or long break)."""
    stype = SessionType(session_type)
    minutes = DEFAULT_DURATIONS[stype]

    labels = {
        SessionType.WORK: "Work",
        SessionType.SHORT_BREAK: "Short Break",
        SessionType.LONG_BREAK: "Long Break",
    }
    label = labels[stype]

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


if __name__ == "__main__":
    main()
