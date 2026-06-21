# test_initial_state.py
"""
Pytest suite to validate the *initial* filesystem state for the
ICMP-reachability summarisation exercise.

This file purposefully checks only the pre-existing **input** artefacts.
It must *not* look for any files or directories that the student is
expected to create later (e.g. summary_report.txt or “processed/”).
"""

import os
import stat
import re
from pathlib import Path

LOG_DIR = Path("/home/user/network/logs")
LOG_15 = LOG_DIR / "ping_results_2023-08-15.log"
LOG_16 = LOG_DIR / "ping_results_2023-08-16.log"

LINE_RE = re.compile(
    r"""
    ^(?P<date>\d{4}-\d{2}-\d{2})        # YYYY-MM-DD
    \s+
    (?P<time>\d{2}:\d{2}:\d{2})         # HH:MM:SS
    \s+Host:\s+
    (?P<ip>(\d{1,3}\.){3}\d{1,3})       # IPv4
    \s+Status:\s+
    (?P<status>alive|unreachable)       # Status
    (?:\s+time=\d+\.\d+ms)?             # Optional RTT
    $
    """,
    re.VERBOSE,
)


def read_lines(path: Path):
    """Return a list of stripped lines from a text file."""
    with path.open("r", encoding="utf-8") as fh:
        return [ln.rstrip("\n") for ln in fh]


def basic_fs_checks(path: Path):
    """Shared assertions that a file exists, is readable and is a regular file."""
    assert path.exists(), f"Required log file missing: {path}"
    assert path.is_file(), f"Expected a regular file at {path}, but found something else."
    mode = path.stat().st_mode
    assert mode & stat.S_IRUSR, f"File {path} is not readable."


def verify_log(path: Path, expected_date: str, expected_total: int, expected_alive: int, expected_down: int):
    """
    Validate:
        1. File system presence and readability.
        2. Each line matches required format.
        3. Stats (total / alive / unreachable) are as expected.
    """
    basic_fs_checks(path)
    lines = read_lines(path)

    assert len(lines) == expected_total, (
        f"{path} should contain {expected_total} probe lines but contains {len(lines)}."
    )

    alive = down = 0
    for lineno, line in enumerate(lines, start=1):
        m = LINE_RE.match(line)
        assert m, f"{path}:{lineno} does not match required log format.\nOffending line: {line!r}"

        date_in_line = m.group("date")
        status = m.group("status")

        assert date_in_line == expected_date, (
            f"{path}:{lineno} has date {date_in_line} but file is expected to contain only {expected_date}."
        )

        if status == "alive":
            alive += 1
            # A time= field must be present for 'alive'
            assert "time=" in line, f"{path}:{lineno} has status 'alive' but no 'time=' field."
        else:  # unreachable
            down += 1
            # Ensure 'time=' field is absent for 'unreachable'
            assert "time=" not in line, f"{path}:{lineno} should not contain 'time=' when status is 'unreachable'."

    assert alive == expected_alive, (
        f"{path} should have {expected_alive} 'alive' entries but has {alive}."
    )
    assert down == expected_down, (
        f"{path} should have {expected_down} 'unreachable' entries but has {down}."
    )
    assert alive + down == expected_total, "Alive + Down counts do not add up to total."


def test_logs_directory_exists_and_is_directory():
    assert LOG_DIR.exists(), f"Log directory {LOG_DIR} is missing."
    assert LOG_DIR.is_dir(), f"{LOG_DIR} exists but is not a directory."


def test_2023_08_15_log_initial_state():
    verify_log(
        path=LOG_15,
        expected_date="2023-08-15",
        expected_total=5,
        expected_alive=3,
        expected_down=2,
    )


def test_2023_08_16_log_initial_state():
    verify_log(
        path=LOG_16,
        expected_date="2023-08-16",
        expected_total=6,
        expected_alive=3,
        expected_down=3,
    )