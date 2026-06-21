# test_initial_state.py
#
# Pytest suite that verifies the *initial* filesystem state
# before the student carries out any log-processing tasks.
#
# The grader expects exactly one existing file:
#   /home/user/app/logs/app.log   (with 8 precise lines)
#
# It also expects that the three artefacts the student must
# create later do *not* exist yet:
#   /home/user/app/logs/errors.log
#   /home/user/app/logs/errors_anon.log
#   /home/user/app/logs/error_summary.tsv
#
# Any deviation from this baseline should cause these tests to fail
# with a clear, actionable message.

import os
from pathlib import Path

LOG_DIR = Path("/home/user/app/logs")
APP_LOG = LOG_DIR / "app.log"
EXPECTED_ARTIFACTS = {
    "errors.log",
    "errors_anon.log",
    "error_summary.tsv",
}

EXPECTED_APP_LOG_LINES = [
    "2023-08-10 12:00:01 INFO 100 RequestID=abc123 User=alice IP=192.168.1.10 Successful login",
    "2023-08-10 12:05:47 ERROR 500 RequestID=def456 User=bob IP=10.0.0.42 NullPointerException at line 42",
    "2023-08-10 12:07:33 WARN 300 RequestID=ghi789 User=carol IP=172.16.5.3 Slow response",
    "2023-08-10 12:12:11 ERROR 404 RequestID=jkl012 User=dave IP=192.168.1.55 Resource not found /favicon.ico",
    "2023-08-10 12:15:27 ERROR 500 RequestID=mno345 User=erin IP=10.0.0.99 NullPointerException at line 87",
    "2023-08-10 12:15:28 INFO 100 RequestID=pqr678 User=frank IP=172.16.5.3 Logout",
    "2023-08-10 12:18:00 ERROR 403 RequestID=stu901 User=gina IP=192.168.1.10 Forbidden access to /admin",
    "2023-08-10 12:19:15 ERROR 404 RequestID=vwx234 User=henry IP=192.168.1.55 Resource not found /robots.txt",
]


def test_log_directory_exists():
    """The directory /home/user/app/logs/ must exist and be a directory."""
    assert LOG_DIR.exists(), f"Required directory not found: {LOG_DIR}"
    assert LOG_DIR.is_dir(), f"{LOG_DIR} exists but is not a directory."


def test_only_app_log_present_initially():
    """
    Before the student starts, the directory must *not* contain the
    artefacts that they are supposed to create.
    """
    missing = [p for p in EXPECTED_ARTIFACTS if (LOG_DIR / p).exists()]
    assert not (LOG_DIR / "errors.log").exists(), "errors.log already exists—remove it before starting the task."
    assert not (LOG_DIR / "errors_anon.log").exists(), "errors_anon.log already exists—remove it before starting the task."
    assert not (LOG_DIR / "error_summary.tsv").exists(), "error_summary.tsv already exists—remove it before starting the task."


def test_app_log_file_and_contents():
    """app.log must exist and contain exactly the 8 expected lines."""
    assert APP_LOG.exists(), f"Required file not found: {APP_LOG}"
    assert APP_LOG.is_file(), f"{APP_LOG} exists but is not a regular file."

    # Read lines without trailing newlines for clean comparison
    with APP_LOG.open("r", encoding="utf-8") as fh:
        actual_lines = [line.rstrip("\n") for line in fh.readlines()]

    assert actual_lines == EXPECTED_APP_LOG_LINES, (
        "Contents of app.log do not match the expected baseline.\n"
        "Differences:\n"
        f"Expected ({len(EXPECTED_APP_LOG_LINES)} lines):\n"
        + "\n".join(EXPECTED_APP_LOG_LINES)
        + "\n\nActual ({len(actual_lines)} lines):\n"
        + "\n".join(actual_lines)
    )