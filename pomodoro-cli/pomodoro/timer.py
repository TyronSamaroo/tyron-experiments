"""Core countdown timer logic."""

import sys
import time
from enum import Enum


class SessionType(str, Enum):
    WORK = "work"
    SHORT_BREAK = "short_break"
    LONG_BREAK = "long_break"


def countdown(total_seconds: int, label: str = "Work") -> bool:
    """
    Run a countdown timer, printing to stdout in-place.

    Returns True if timer completed normally, False if interrupted.
    """
    try:
        for remaining in range(total_seconds, -1, -1):
            minutes, seconds = divmod(remaining, 60)
            bar_filled = int((total_seconds - remaining) / total_seconds * 20)
            bar = "#" * bar_filled + "-" * (20 - bar_filled)
            line = f"\r[{label}]  [{bar}]  {minutes:02d}:{seconds:02d} remaining  "
            sys.stdout.write(line)
            sys.stdout.flush()
            if remaining > 0:
                time.sleep(1)
        sys.stdout.write("\n")
        return True
    except KeyboardInterrupt:
        sys.stdout.write("\n")
        return False
