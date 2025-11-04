# Habit Hub

Habit Hub is an interactive Textual dashboard that gives a rich overview of the data captured by the existing Macro Tracker CLI. It surfaces your macro targets, daily consumption, and weight trends in a responsive terminal UI with quick filters and editing tools.

## Features

- **Daily macro dashboard** – browse any logged day and instantly see calories, macros, remaining targets, and progress bars.
- **Food timeline** – view each food entry with timestamp, macro breakdown, and totals.
- **Weight trends** – lightweight sparkline highlights recent progress and deltas from your starting weight.
- **Quick logging** – capture a food entry directly inside Habit Hub without leaving the dashboard.
- **Live reload** – press `r` to refresh the view from the JSON data file.

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommended) or `pip`

## Installation

```bash
cd habit-hub
uv sync
```

Alternatively, install with pip:

```bash
pip install -e .
```

## Usage

```bash
uv run habit-hub
```

or, if installed via pip:

```bash
python -m habit_hub
```

### Keyboard shortcuts

| Key | Action |
| --- | ------ |
| `q` | Quit the dashboard |
| `r` | Reload data from `~/.macro_tracker.json` |
| `n` | Open the "Quick Log" modal to capture a food entry |

Buttons for switching tabs and the date list can also be navigated with arrow keys/enter.

## Data Source

Habit Hub reads from the same file used by the Macro Tracker CLI: `~/.macro_tracker.json`. The dashboard expects the structure created by the CLI, but it gracefully handles missing data by showing empty states.

## Development

To run the Textual dev server with hot reload:

```bash
uv run textual run habit_hub/dashboard.py --dev
```

The app uses [Textual](https://textual.textualize.io/) widgets and simple modular components defined in `habit_hub/dashboard.py`.

