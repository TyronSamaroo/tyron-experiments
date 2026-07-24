"""Tests for loading, saving, and resetting Pomodoro configuration."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from pomodoro.config import DEFAULTS, load_config, reset_config, save_config


class ConfigTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.config_path = Path(self.temp_dir.name) / "config.json"
        self.path_patch = patch("pomodoro.config.CONFIG_PATH", self.config_path)
        self.path_patch.start()
        self.addCleanup(self.path_patch.stop)

    def test_missing_file_returns_independent_defaults(self) -> None:
        config = load_config()
        config["work_minutes"] = 99

        self.assertEqual(DEFAULTS["work_minutes"], 25)
        self.assertEqual(load_config(), DEFAULTS)

    def test_load_merges_saved_values_with_new_defaults(self) -> None:
        self.config_path.write_text(
            json.dumps({"work_minutes": 50}),
            encoding="utf-8",
        )

        self.assertEqual(
            load_config(),
            {
                "work_minutes": 50,
                "short_break_minutes": 5,
                "long_break_minutes": 15,
            },
        )

    def test_save_and_reset_write_readable_json(self) -> None:
        save_config(
            {
                "work_minutes": 40,
                "short_break_minutes": 8,
                "long_break_minutes": 20,
            }
        )

        self.assertTrue(self.config_path.read_text(encoding="utf-8").endswith("\n"))
        self.assertEqual(load_config()["work_minutes"], 40)

        reset_config()

        self.assertEqual(load_config(), DEFAULTS)


if __name__ == "__main__":
    unittest.main()
