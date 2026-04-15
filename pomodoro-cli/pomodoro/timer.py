"""Core countdown timer logic."""

import signal
import sys
import time
from enum import Enum
from typing import Optional

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

_interrupted = False


def _handle_sigint(signum, frame):
    """Set a flag on SIGINT rather than raising immediately."""
    global _interrupted
    _interrupted = True


def countdown(total_seconds: int, label: str = "Work") -> bool:
    """
    Run a countdown timer, printing to stdout in-place with color.

    Handles Ctrl+C gracefully: prints a cancellation notice and returns False.
    Returns True if timer completed normally, False if interrupted.
    """
    global _interrupted
    _interrupted = False

    color = SESSION_COLORS.get(label, Fore.WHITE)

    # Install custom SIGINT handler so we can print a clean line before exiting
    original_handler = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, _handle_sigint)

    completed = False
    try:
        for remaining in range(total_seconds, -1, -1):
            if _interrupted:
                break

            minutes, seconds = divmod(remaining, 60)
            bar_filled = int((total_seconds - remaining) / total_seconds * 20)
            bar = (
                color + "#" * bar_filled
                + Style.DIM + "-" * (20 - bar_filled)
                + Style.RESET_ALL
            )
            time_str = color + f"{minutes:02d}:{seconds:02d}" + Style.RESET_ALL
            label_str = color + Style.BRIGHT + f"[{label}]" + Style.RESET_ALL
            hint = f"{Style.DIM}  (Ctrl+C to cancel){Style.RESET_ALL}" if remaining == total_seconds else ""
            line = f"\r{label_str}  [{bar}]  {time_str} remaining{hint}  "
            sys.stdout.write(line)
            sys.stdout.flush()

            if remaining > 0:
                time.sleep(1)

        completed = not _interrupted
        if completed:
            sys.stdout.write("\n")
        else:
            elapsed = total_seconds - remaining  # type: ignore[possibly-undefined]
            elapsed_min, elapsed_sec = divmod(elapsed, 60)
            sys.stdout.write(
                f"\n{Fore.YELLOW}Cancelled after {elapsed_min}m {elapsed_sec}s.{Style.RESET_ALL}\n"
            )
    finally:
        signal.signal(signal.SIGINT, original_handler)

    return completed
