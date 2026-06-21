# test_initial_state.py
#
# Pytest suite that validates the initial, pre-task filesystem state.
# It checks that the log directory and log file exist and that the file
# contents are exactly as specified in the task description.
#
# NOTE:  We deliberately do NOT touch /home/user/output/ or any deliverable
#        files.  This file is concerned only with the state that must be
#        present *before* the student begins their work.

import os
from pathlib import Path

LOG_DIR = Path("/home/user/logs")
LOG_FILE = LOG_DIR / "app.log"

# Expected log lines (each MUST end with a single '\n').
EXPECTED_LINES = [
    "2023-08-21T14:32:07Z ERROR Failed login for user 'admin' from 10.0.0.23\n",
    "2023-08-21T14:33:58Z INFO User 'alice' authenticated successfully from 10.0.0.11\n",
    "2023-08-21T14:34:12Z WARN Unauthorized access attempt to /secure/data by user 'bob'\n",
    "2023-08-21T14:35:47Z ERROR Reflected XSS attempt detected in parameter 'q'\n",
    "2023-08-21T14:36:02Z DEBUG Cache miss for key 'session_123'\n",
    "2023-08-21T14:36:15Z INFO User 'alice' logged out\n",
    "2023-08-21T14:37:00Z WARN Rate limit exceeded for IP 10.0.0.23\n",
]


def test_logs_directory_exists():
    """
    Verify that /home/user/logs exists and is a directory with readable
    permissions for the current user.
    """
    assert LOG_DIR.exists(), f"Required directory {LOG_DIR} is missing."
    assert LOG_DIR.is_dir(), f"{LOG_DIR} exists but is not a directory."
    # Basic permission sanity-check: current user must be able to list it.
    try:
        list(LOG_DIR.iterdir())
    except PermissionError as exc:
        pytest.fail(f"Permission denied when accessing {LOG_DIR}: {exc}")


def test_app_log_file_exists():
    """
    Verify that the log file exists, is a regular file, and is readable.
    """
    assert LOG_FILE.exists(), f"Required log file {LOG_FILE} is missing."
    assert LOG_FILE.is_file(), f"{LOG_FILE} exists but is not a regular file."
    assert os.access(LOG_FILE, os.R_OK), f"Log file {LOG_FILE} is not readable."


def test_app_log_file_content_exact_match():
    """
    The log file must contain exactly the seven expected lines (including
    trailing newlines) and nothing else.
    """
    actual_lines = LOG_FILE.read_text(encoding="utf-8").splitlines(keepends=True)

    # Fail fast on line-count mismatch
    assert (
        len(actual_lines) == len(EXPECTED_LINES)
    ), (
        f"{LOG_FILE} should contain {len(EXPECTED_LINES)} lines but has "
        f"{len(actual_lines)}.\nActual lines:\n{''.join(actual_lines)}"
    )

    # Compare each line for an exact match
    for idx, (expected, actual) in enumerate(zip(EXPECTED_LINES, actual_lines), start=1):
        assert (
            actual == expected
        ), (
            f"Mismatch on line {idx} of {LOG_FILE}.\n"
            f"Expected: {expected!r}\n"
            f"Actual:   {actual!r}"
        )