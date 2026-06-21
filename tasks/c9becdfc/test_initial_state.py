# test_initial_state.py
#
# Pytest suite that validates the expected *initial* filesystem state
# before the student runs any command.
#
# DO NOT EDIT THE PATHS – the autograder relies on these exact values.
# ---------------------------------------------------------------------

import os
import stat
import time
import pathlib

import pytest


# ---------------------------------------------------------------------
# Paths that must already exist
# ---------------------------------------------------------------------
BASE_DIR = pathlib.Path("/home/user/microservices/logs")
SERVICE_A_DIR = BASE_DIR / "serviceA"
SERVICE_B_DIR = BASE_DIR / "serviceB"

OLD_LOGS = [
    SERVICE_A_DIR / "access-2023-01-10.log",
    SERVICE_A_DIR / "error-2023-01-09.log",
    SERVICE_B_DIR / "app-2023-01-08.log",
]

RECENT_LOGS = [
    SERVICE_A_DIR / "current.log",
    SERVICE_B_DIR / "debug-2023-12-31.log",
]

REPORT_FILE = pathlib.Path("/home/user/deleted_logs_report.txt")

# Threshold in seconds for "older than 7 days"
SEVEN_DAYS = 7 * 24 * 60 * 60


# ---------------------------------------------------------------------
# Helper assertions
# ---------------------------------------------------------------------
def _assert_regular_file(p: pathlib.Path, msg: str) -> None:
    assert p.exists(), f"{msg}: expected path '{p}' to exist"
    assert p.is_file(), f"{msg}: expected '{p}' to be a regular file"


# ---------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------
def test_directories_exist():
    """Required service log directories must be present and searchable."""
    for d in (SERVICE_A_DIR, SERVICE_B_DIR):
        assert d.exists(), f"Directory '{d}' is missing"
        assert d.is_dir(), f"'{d}' exists but is not a directory"
        # Basic permission check: owner must have read+execute so that the tests can traverse
        mode = d.stat().st_mode
        assert mode & stat.S_IRUSR, f"Owner does not have read permission on '{d}'"
        assert mode & stat.S_IXUSR, f"Owner does not have execute/search permission on '{d}'"


def test_old_logs_present_and_old():
    """The three rotated log files must exist and be older than 7 days."""
    now = time.time()
    for p in OLD_LOGS:
        _assert_regular_file(p, "Old log missing")
        age = now - p.stat().st_mtime
        assert (
            age > SEVEN_DAYS
        ), f"Expected '{p}' to be older than 7 days, but it is only {age/86400:.2f} days old"


def test_recent_logs_present_and_recent():
    """The two newer log files must exist and be 7 days old or newer."""
    now = time.time()
    for p in RECENT_LOGS:
        _assert_regular_file(p, "Recent log missing")
        age = now - p.stat().st_mtime
        assert (
            age <= SEVEN_DAYS
        ), f"Expected '{p}' to be 7 days old or newer, but it is {age/86400:.2f} days old"


def test_report_file_absent_initially():
    """The deletion report must NOT exist before the student runs the command."""
    assert (
        not REPORT_FILE.exists()
    ), f"'{REPORT_FILE}' already exists—remove it before executing your solution"