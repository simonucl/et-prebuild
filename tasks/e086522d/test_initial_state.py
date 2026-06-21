# test_initial_state.py
"""
Pytest suite to validate the initial operating-system / filesystem state
before the student runs any commands for the “ERROR line extraction” task.

This file checks ONLY the pre-existing resources (input log file, directory
permissions, etc.).  It deliberately avoids touching or asserting anything
about the output artefacts that the student is expected to create later.
"""

import os
from pathlib import Path
import stat
import pytest

# ---------------------------------------------------------------------------
# Constants describing the expected initial state
# ---------------------------------------------------------------------------

LOG_DIR = Path("/home/user/app/logs")
APP_LOG = LOG_DIR / "app.log"

# The exact, canonical content of /home/user/app/logs/app.log
EXPECTED_APP_LOG_CONTENT = (
    "2023-08-20 11:37:02 INFO Starting service\n"
    "2023-08-20 11:37:05 WARN Config file not found, using defaults\n"
    "2023-08-20 11:37:10 ERROR Failed to connect to database\n"
    "2023-08-20 11:37:12 INFO Retrying connection\n"
    "2023-08-20 11:37:15 ERROR Failed to connect to database\n"
    "2023-08-20 11:37:18 INFO Giving up after 3 retries\n"
    "2023-08-20 11:37:20 ERROR Service terminated unexpectedly\n"
    "2023-08-20 11:37:22 INFO Shutdown complete\n"
)

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def _is_writable(path: Path) -> bool:
    """
    Return True if the current user has write permission to *path*.
    For directories this means we can create files inside it.
    """
    return os.access(path, os.W_OK)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_logs_directory_exists_and_writable():
    """
    The directory /home/user/app/logs must exist, be a directory, and be
    writable by the current user so the student can create error_summary.log.
    """
    assert LOG_DIR.exists(), (
        f"Required directory {LOG_DIR} is missing. "
        "Create it with the correct path and permissions."
    )
    assert LOG_DIR.is_dir(), (
        f"{LOG_DIR} exists but is not a directory."
    )

    assert _is_writable(LOG_DIR), (
        f"The directory {LOG_DIR} is not writable by the current user. "
        "Adjust its permissions (chmod) or ownership so files can be written."
    )


def test_app_log_exists_with_exact_content_and_unix_lf():
    """
    The input log file must exist, be encoded in UTF-8, end with a single LF,
    contain only Unix line endings, and match the exact expected content.
    """
    assert APP_LOG.exists(), (
        f"Log file {APP_LOG} does not exist. "
        "Ensure the log file is present before running the extraction command."
    )
    assert APP_LOG.is_file(), f"{APP_LOG} exists but is not a regular file."

    # Read as bytes first so we can inspect raw newline characters
    raw_bytes = APP_LOG.read_bytes()

    # 1. It must decode as UTF-8
    try:
        content = raw_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        pytest.fail(
            f"{APP_LOG} is not valid UTF-8: {exc}. "
            "Recreate the file with UTF-8 encoding."
        )

    # 2. No Windows CRLF line endings should be present
    assert b"\r\n" not in raw_bytes, (
        f"{APP_LOG} must use Unix LF (\\n) line endings only; "
        "found Windows CRLF (\\r\\n)."
    )

    # 3. The file must end with a single LF
    assert content.endswith("\n"), (
        f"{APP_LOG} must end with a single newline (LF)."
    )

    # 4. The entire file content must match the expected truth value
    assert content == EXPECTED_APP_LOG_CONTENT, (
        f"{APP_LOG} does not match the expected initial content.\n"
        "Differences may indicate the file was modified or corrupted."
    )

    # 5. Sanity-check: there should be exactly three lines containing 'ERROR'
    error_lines = [line for line in content.splitlines() if "ERROR" in line]
    assert len(error_lines) == 3, (
        f"Expected 3 lines containing the exact string 'ERROR' in {APP_LOG}; "
        f"found {len(error_lines)}."
    )