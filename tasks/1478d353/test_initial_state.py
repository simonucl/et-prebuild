# test_initial_state.py
#
# This pytest suite verifies that the *initial* environment is set up
# correctly before the student attempts the task.  It intentionally
# does NOT look for any artefacts that the student must create.
#
# Assumptions spelled-out in the public task description:
#   * The home directory is /home/user
#   * The application log is located at
#         /home/user/monitoring/logs/service.log
#   * The student will later create files under
#         /home/user/monitoring/alerts/
#
# Only stdlib + pytest are used.

import re
from pathlib import Path

import pytest


HOME = Path("/home/user")
LOG_DIR = HOME / "monitoring" / "logs"
LOG_FILE = LOG_DIR / "service.log"


@pytest.fixture(scope="module")
def log_lines():
    """Return the list of lines in the service log (stripped of trailing newlines)."""
    with LOG_FILE.open("r", encoding="utf-8") as f:
        # Keep the newline characters out for easier asserts later on
        return [line.rstrip("\n") for line in f.readlines()]


def test_log_directory_exists():
    assert LOG_DIR.is_dir(), (
        f"Expected log directory '{LOG_DIR}' to exist and be a directory, "
        "but it was not found."
    )


def test_service_log_exists():
    assert LOG_FILE.is_file(), (
        f"Expected log file '{LOG_FILE}' to exist, but it was not found."
    )


def test_service_log_not_empty(log_lines):
    assert log_lines, (
        f"Log file '{LOG_FILE}' appears to be empty. "
        "It should contain historical log entries."
    )


def test_log_contains_error_lines(log_lines):
    error_lines = [ln for ln in log_lines if "ERROR" in ln]
    assert error_lines, (
        f"No lines containing the string 'ERROR' were found in '{LOG_FILE}'. "
        "The assignment relies on at least some ERROR events being present."
    )


def test_error_lines_cover_expected_hours(log_lines):
    """
    The public specification and sample data suggest that ERROR entries
    span the hours 14, 15, and 16.  We validate that those hours are
    indeed represented so the student’s subsequent counting work makes
    sense.

    The timestamp format is assumed to be:
        YYYY-MM-DD HH:MM:SS <LEVEL> <message…>
    """
    hour_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}\s+(\d{2}):\d{2}:\d{2}\s+ERROR\b")

    hours_with_errors = {
        int(match.group(1))
        for line in log_lines
        for match in [hour_pattern.match(line)]
        if match
    }

    expected_hours = {14, 15, 16}
    missing = expected_hours - hours_with_errors
    assert not missing, (
        "The log file is missing ERROR entries for the following expected "
        f"hour(s): {sorted(missing)}.\n"
        f"Found hours with ERROR entries: {sorted(hours_with_errors)}"
    )