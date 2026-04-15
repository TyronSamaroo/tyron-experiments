"""User config stored as a simple JSON file at ~/.pomodoro_config.json."""

import json
from pathlib import Path

CONFIG_PATH = Path.home() / ".pomodoro_config.json"

DEFAULTS = {
    "work_minutes": 25,
    "short_break_minutes": 5,
    "long_break_minutes": 15,
}


def load_config() -> dict:
    """Load config from disk, falling back to defaults for missing keys."""
    if not CONFIG_PATH.exists():
        return dict(DEFAULTS)
    with CONFIG_PATH.open() as f:
        data = json.load(f)
    # Merge with defaults so new keys always exist
    return {**DEFAULTS, **data}


def save_config(cfg: dict) -> None:
    with CONFIG_PATH.open("w") as f:
        json.dump(cfg, f, indent=2)


def reset_config() -> None:
    save_config(dict(DEFAULTS))
