# test_initial_state.py
#
# This pytest suite verifies that the operating-system / filesystem
# is in the expected **initial** state _before_ the student performs
# any actions.  It focuses on the directory layout, the presence and
# exact contents of the raw authentication logs, and the absence of
# any report artefacts that the student is supposed to create later.
#
# Only the Python standard library and pytest are used.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
RAW_DIR = HOME / "audit" / "raw"
REPORTS_DIR = HOME / "audit" / "reports"

LOG_10 = RAW_DIR / "auth_2024-06-10.log"
LOG_11 = RAW_DIR / "auth_2024-06-11.log"
LOG_12 = RAW_DIR / "auth_2024-06-12.log"

UNIQUE_USER_IP = REPORTS_DIR / "unique_user_ip.tsv"
COMMAND_LOG = REPORTS_DIR / "command_log.txt"


@pytest.fixture(scope="module")
def expected_log_contents():
    """Return a dict mapping log Path objects to their exact expected contents."""
    return {
        LOG_10: (
            "2024-06-10T09:15:23Z alice 192.168.1.5 SUCCESS\n"
            "2024-06-10T09:17:45Z bob 10.0.0.12 FAILURE\n"
            "2024-06-10T10:01:02Z charlie 172.16.0.3 SUCCESS\n"
            "2024-06-10T11:20:00Z alice 192.168.1.5 FAILURE\n"
        ),
        LOG_11: (
            "2024-06-11T08:05:12Z bob 10.0.0.12 SUCCESS\n"
            "2024-06-11T09:55:30Z dave 203.0.113.45 SUCCESS\n"
            "2024-06-11T10:00:00Z alice 192.168.1.5 SUCCESS\n"
        ),
        LOG_12: (
            "2024-06-12T07:45:22Z charlie 172.16.0.3 FAILURE\n"
            "2024-06-12T08:33:00Z eve 198.51.100.17 SUCCESS\n"
            "2024-06-12T09:00:00Z alice 192.168.1.5 SUCCESS\n"
        ),
    }


# ---------------------------------------------------------------------------
# Directory-level tests
# ---------------------------------------------------------------------------


def test_required_directories_exist_and_are_dirs():
    assert RAW_DIR.is_dir(), f"Expected raw directory {RAW_DIR} to exist and be a directory."
    assert REPORTS_DIR.is_dir(), f"Expected reports directory {REPORTS_DIR} to exist and be a directory."


def test_reports_directory_initially_empty():
    # The student must populate this directory later; for now it should be empty.
    contents = [p for p in REPORTS_DIR.iterdir()]
    assert contents == [], (
        f"{REPORTS_DIR} is expected to be empty before the exercise starts, "
        f"but found: {', '.join(map(str, contents))}"
    )


# ---------------------------------------------------------------------------
# Raw log file tests
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("log_path", [LOG_10, LOG_11, LOG_12])
def test_raw_logs_exist(log_path):
    assert log_path.is_file(), f"Expected log file {log_path} to exist."


def test_raw_log_contents_exact_match(expected_log_contents):
    for path, expected in expected_log_contents.items():
        with path.open("r", encoding="utf-8") as fh:
            actual = fh.read()
        assert (
            actual == expected
        ), f"Contents of {path} do not match expected initial state.\n--- Expected ---\n{expected}\n--- Actual ---\n{actual}"


# ---------------------------------------------------------------------------
# Absence of artefacts that the student must create
# ---------------------------------------------------------------------------


def test_unique_user_ip_not_yet_created():
    assert not UNIQUE_USER_IP.exists(), (
        f"{UNIQUE_USER_IP} should NOT exist before the student starts the task."
    )


def test_command_log_not_yet_created():
    assert not COMMAND_LOG.exists(), (
        f"{COMMAND_LOG} should NOT exist before the student starts the task."
    )