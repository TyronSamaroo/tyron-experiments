"""Core countdown timer logic."""

import sys
import time
from enum import Enum

from colorama import Fore, Style, init as colorama_init

colorama_init(autoreset=True)


class SessionType(str, Enum):
    WORK = "work"
    SHORT_BREAK = "short_break"
    LONG_BREAK = "long_break"


# Color scheme per session type
SESSION_COLORS = {
    "Work": Fore.RED,
    "Short Break": Fore.GREEN,
    "Long Break": Fore.CYAN,
}


def countdown(total_seconds: int, label: str = "Work") -> bool:
    """
    Run a countdown timer, printing to stdout in-place with color.

    Returns True if timer completed normally, False if interrupted.
    """
    color = SESSION_COLORS.get(label, Fore.WHITE)
    try:
        for remaining in range(total_seconds, -1, -1):
            minutes, seconds = divmod(remaining, 60)
            bar_filled = int((total_seconds - remaining) / total_seconds * 20)
            bar = (
                color + "#" * bar_filled
                + Style.DIM + "-" * (20 - bar_filled)
                + Style.RESET_ALL
            )
            time_str = color + f"{minutes:02d}:{seconds:02d}" + Style.RESET_ALL
            label_str = color + Style.BRIGHT + f"[{label}]" + Style.RESET_ALL
            line = f"\r{label_str}  [{bar}]  {time_str} remaining  "
            sys.stdout.write(line)
            sys.stdout.flush()
            if remaining > 0:
                time.sleep(1)
        sys.stdout.write("\n")
        return True
    except KeyboardInterrupt:
        sys.stdout.write("\n")
        return False
