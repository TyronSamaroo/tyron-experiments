"""Entry point for the pomodoro CLI."""

import click


@click.group()
def main():
    """Pomodoro CLI — stay focused, track your sessions."""
    pass


@main.command()
def start():
    """Start a Pomodoro session."""
    click.echo("Pomodoro timer — coming soon!")


if __name__ == "__main__":
    main()
