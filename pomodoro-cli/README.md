# pomodoro-cli

A terminal-based Pomodoro timer with session history, stats, and streak tracking.

> Work in progress — see commit history for incremental build.

## Setup

```bash
uv venv && source .venv/bin/activate
uv pip install -e .
```

## Usage

```bash
pomodoro start          # start a 25-min work session
pomodoro start --short  # 5-min short break
pomodoro start --long   # 15-min long break
pomodoro stats          # view session history and streaks
pomodoro config         # show/edit timer durations
```
