"""Entry point for the pomodoro CLI."""

import click
from pomodoro.timer import countdown

WORK_MINUTES = 25


@click.group()
def main():
    """Pomodoro CLI — stay focused, track your sessions."""
    pass


@main.command()
def start():
    """Start a 25-minute work session."""
    click.echo(f"Starting {WORK_MINUTES}-minute Pomodoro. Press Ctrl+C to cancel.\n")
    completed = countdown(WORK_MINUTES * 60, label="Work")
    if completed:
        click.echo("Session complete! Take a break.")
    else:
        click.echo("Session cancelled.")


if __name__ == "__main__":
    main()
