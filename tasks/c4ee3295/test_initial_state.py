# test_initial_state.py
#
# This test-suite verifies that the expected **initial** filesystem state
# is present *before* the student runs any commands.  It purposely does
# NOT look for the output file that the task asks the student to create.
#
# The checks performed are:
#   1. The directory /home/user/logs exists and is a directory.
#   2. The file   /home/user/logs/app.log exists, is a file,
#      and contains the exact expected content (byte-for-byte).

import pytest
from pathlib import Path


LOGS_DIR = Path("/home/user/logs")
APP_LOG   = LOGS_DIR / "app.log"

# --------------------------------------------------------------------------- #
# Helpers                                                                     #
# --------------------------------------------------------------------------- #
_EXPECTED_APP_LOG_LINES = [
    "2023-08-15 13:45:12,123 INFO  Request from 10.0.0.1 processed in 120ms\n",
    "2023-08-15 14:00:03,001 ERROR Database connection failed for user app\n",
    "2023-08-15 14:12:55,789 WARN  Cache miss for key user_42\n",
    "2023-08-15 14:22:11,456 ERROR Timeout while calling external API\n",
    "2023-08-15 14:45:00,999 FATAL Unhandled exception in payment service\n",
    "2023-08-15 15:00:00,000 INFO  Scheduled job started\n",
    "2023-08-14 14:30:32,222 ERROR Previous day error.\n",
]


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #
def test_logs_directory_exists():
    """/home/user/logs must be an existing directory."""
    assert LOGS_DIR.exists(), f"Missing directory: {LOGS_DIR}"
    assert LOGS_DIR.is_dir(), f"{LOGS_DIR} exists but is not a directory"


def test_app_log_file_exists_and_contents_are_correct():
    """
    /home/user/logs/app.log must exist and contain the exact expected
    lines in the exact order.  If this test fails, the most common cause
    is that the file was accidentally modified or truncated.
    """
    # --- Existence & type checks ------------------------------------------------
    assert APP_LOG.exists(), f"Missing file: {APP_LOG}"
    assert APP_LOG.is_file(), f"{APP_LOG} exists but is not a regular file"

    # --- Content check ----------------------------------------------------------
    with APP_LOG.open("r", encoding="utf-8") as fp:
        actual_lines = fp.readlines()

    assert actual_lines == _EXPECTED_APP_LOG_LINES, (
        f"{APP_LOG} does not match the expected initial content.\n"
        "Please ensure you are starting from the unmodified file provided "
        "in the task description."
    )