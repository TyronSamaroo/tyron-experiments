# pomodoro-cli

A terminal-based Pomodoro timer with session history, streak tracking, and configurable durations — built with Python, Click, and Colorama.

## Features

- **Three session types**: work (25 min), short break (5 min), long break (15 min)
- **Colored progress bar** that ticks down in real time
- **Graceful cancellation** — Ctrl+C records the partial session and shows elapsed time
- **SQLite history** persisted to `~/.pomodoro_sessions.db`
- **Streak tracking** — consecutive days with at least one completed work session
- **Daily summary** — today's Pomodoro count and focused minutes at a glance
- **JSON config** at `~/.pomodoro_config.json` for custom durations

## Setup

```bash
# Requires Python 3.10+
uv venv && source .venv/bin/activate
uv pip install -e .
```

Or with pip:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .
```

## Usage

```bash
# Start sessions
pomodoro start           # 25-min work session (default)
pomodoro start --short   # 5-min short break
pomodoro start --long    # 15-min long break

# View history & stats
pomodoro stats           # streak, daily summary, recent sessions table
pomodoro stats --limit 50  # show last 50 sessions

# Configure durations
pomodoro config                    # show current durations
pomodoro config --work 50          # set work to 50 minutes
pomodoro config --short 10         # set short break to 10 minutes
pomodoro config --long 20          # set long break to 20 minutes
pomodoro config --reset            # restore defaults
```

## Project Structure

```
pomodoro-cli/
├── pyproject.toml          # deps: click, colorama
└── pomodoro/
    ├── __init__.py
    ├── cli.py              # Click commands: start, stats, config
    ├── timer.py            # Countdown loop + SIGINT handling + SessionType enum
    ├── db.py               # SQLite CRUD (init, save, fetch)
    ├── stats.py            # Formatting, streak, daily summary
    └── config.py           # JSON config load/save/reset
```

## Data Files

| File | Purpose |
|------|---------|
| `~/.pomodoro_sessions.db` | SQLite session history |
| `~/.pomodoro_config.json` | Custom timer durations |

## Tech Stack

- **Python 3.10+**
- **[Click](https://click.palletsprojects.com/)** — CLI framework
- **[Colorama](https://pypi.org/project/colorama/)** — cross-platform ANSI colors
- **sqlite3** — stdlib, no extra deps
- **uv** — fast Python package manager
