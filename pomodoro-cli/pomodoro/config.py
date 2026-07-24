"""User config stored as a simple JSON file at ~/.pomodoro_config.json."""

import json
from pathlib import Path

CONFIG_PATH = Path.home() / ".pomodoro_config.json"

DEFAULTS = {
    "work_minutes": 25,
    "short_break_minutes": 5,
    "long_break_minutes": 15,
}


def load_config() -> dict[str, int]:
    """Load config from disk, falling back to defaults for missing keys."""
    if not CONFIG_PATH.exists():
        return dict(DEFAULTS)
    with CONFIG_PATH.open(encoding="utf-8") as f:
        data = json.load(f)

    # Preserve older config files when a new setting is added to DEFAULTS.
    return {**DEFAULTS, **data}


def save_config(cfg: dict[str, int]) -> None:
    """Write config as stable, human-readable UTF-8 JSON."""
    with CONFIG_PATH.open("w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)
        f.write("\n")


def reset_config() -> None:
    """Replace saved values with a fresh copy of the defaults."""
    save_config(dict(DEFAULTS))
