# test_initial_state.py
#
# This pytest file verifies that the operating-system / filesystem state
# *before* the student performs any action is exactly as expected for the
# assignment “log the latest training-run metrics”.
#
# It checks:
#   • The experiment directory exists.
#   • metrics.csv exists and contains the expected header and data lines.
#   • latest_metrics.log does *not* exist yet.
#
# Any failure message is written to help the student (or the autograder)
# immediately understand what is missing or incorrect.

import os
from pathlib import Path

import pytest

EXP_DIR = Path("/home/user/experiments/exp_v1")
CSV_FILE = EXP_DIR / "metrics.csv"
LOG_FILE = EXP_DIR / "latest_metrics.log"

EXPECTED_CSV_LINES = [
    "epoch,loss,accuracy",
    "1,0.678,0.75",
    "2,0.432,0.82",
    "3,0.321,0.86",
]


def _read_nonempty_lines(path: Path):
    """Return a list of non-empty lines stripped of their trailing newlines."""
    with path.open("r", encoding="utf-8") as f:
        return [line.rstrip("\n\r") for line in f if line.strip() != ""]


def test_experiment_directory_exists():
    assert EXP_DIR.is_dir(), (
        f"Expected experiment directory does not exist: {EXP_DIR}\n"
        "Create this directory and place metrics.csv inside it."
    )


def test_metrics_csv_presence():
    assert CSV_FILE.is_file(), (
        f"metrics.csv is missing at {CSV_FILE}.\n"
        "Make sure the historical metrics CSV is present before running the task."
    )


def test_metrics_csv_contents():
    lines = _read_nonempty_lines(CSV_FILE)
    assert lines == EXPECTED_CSV_LINES, (
        f"metrics.csv content mismatch.\n"
        f"Expected lines:\n{EXPECTED_CSV_LINES}\n"
        f"Found lines:\n{lines}"
    )
    # Explicitly check the last line so that the failure message is clear.
    expected_last = EXPECTED_CSV_LINES[-1]
    found_last = lines[-1] if lines else "(file empty)"
    assert found_last == expected_last, (
        f"Last line of metrics.csv is incorrect.\n"
        f"Expected: {expected_last!r}\n"
        f"Found   : {found_last!r}"
    )


def test_latest_metrics_log_absence():
    assert not LOG_FILE.exists(), (
        f"{LOG_FILE} already exists, but it should be created *by* the solution "
        "script, not beforehand. Remove or rename this file and re-run the tests."
    )