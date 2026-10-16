"""Regression tests for Pomodoro session statistics."""

import unittest
from datetime import date, datetime, time, timedelta

from pomodoro.db import Session
from pomodoro.stats import current_streak, daily_summary, sessions_by_day


def make_session(
    day: date,
    *,
    session_type: str = "work",
    completed: bool = True,
    duration_minutes: int = 25,
) -> Session:
    """Build an in-memory session without touching the user's SQLite history."""
    started_at = datetime.combine(day, time(hour=9)).isoformat()
    ended_at = datetime.combine(day, time(hour=9, minute=duration_minutes)).isoformat()
    return Session(
        id=1,
        session_type=session_type,
        started_at=started_at,
        ended_at=ended_at,
        completed=completed,
        duration_minutes=duration_minutes,
    )


class SessionStatsTests(unittest.TestCase):
    def test_sessions_by_day_groups_local_iso_dates(self) -> None:
        today = date.today()
        yesterday = today - timedelta(days=1)
        sessions = [
            make_session(today),
            make_session(today, session_type="short_break"),
            make_session(yesterday),
        ]

        grouped = sessions_by_day(sessions)

        self.assertEqual(len(grouped[today]), 2)
        self.assertEqual(len(grouped[yesterday]), 1)

    def test_current_streak_counts_completed_work_through_today(self) -> None:
        today = date.today()
        sessions = [
            make_session(today),
            make_session(today - timedelta(days=1)),
            make_session(today - timedelta(days=2)),
            make_session(today - timedelta(days=3), completed=False),
        ]

        self.assertEqual(current_streak(sessions), 3)

    def test_current_streak_can_carry_from_yesterday(self) -> None:
        today = date.today()
        sessions = [
            make_session(today - timedelta(days=1)),
            make_session(today - timedelta(days=2)),
        ]

        self.assertEqual(current_streak(sessions), 2)

    def test_daily_summary_uses_only_completed_work_sessions(self) -> None:
        target = date(2026, 7, 24)
        sessions = [
            make_session(target, duration_minutes=25),
            make_session(target, duration_minutes=35),
            make_session(target, duration_minutes=20, completed=False),
            make_session(target, session_type="short_break", duration_minutes=5),
        ]

        summary = daily_summary(sessions, target)

        self.assertIn("2 Pomodoros", summary)
        self.assertIn("1h 0m of focused work", summary)


if __name__ == "__main__":
    unittest.main()
