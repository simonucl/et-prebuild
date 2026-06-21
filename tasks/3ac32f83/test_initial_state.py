# test_initial_state.py
#
# Pytest suite that verifies the initial OS / filesystem state
# BEFORE the student performs any actions for the “error-diagnostics”
# exercise.  All checks use absolute paths and standard-library
# functionality only.

import os
import stat
import pytest
from textwrap import dedent

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SUPPORT_DIR = "/home/user/support"
LOGS_DIR = "/home/user/support/logs"
APP_LOG   = "/home/user/support/logs/app.log"
DIAG_DIR  = "/home/user/support/diagnostics"
ERRORS_LOG = "/home/user/support/diagnostics/errors.log"
COLLECTION_LOG = "/home/user/support/diagnostics/collection.log"

EXPECTED_APPLOG_LINES = [
    "2023-10-15 10:15:42,123 INFO  main      REQ-000101 Starting service",
    "2023-10-15 10:16:05,675 ERROR main      REQ-000102 Failed to connect to database",
    "2023-10-15 10:16:07,101 WARN  worker-1  REQ-000103 Retrying",
    "2023-10-15 10:16:10,333 ERROR worker-1  REQ-000104 Timeout reached during operation",
    "2023-10-15 10:16:12,890 INFO  main      REQ-000105 Health check passed",
    "2023-10-15 10:16:15,200 ERROR worker-2  REQ-000106 Null pointer exception",
    "2023-10-15 10:16:16,400 INFO  worker-2  REQ-000107 Shutdown complete",
]

DIR_MODE  = 0o755
FILE_MODE = 0o644


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _mode_bits(path: str) -> int:
    """Return the low permission bits (e.g. 0o755) of a file or directory."""
    return stat.S_IMODE(os.lstat(path).st_mode)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_support_directory_exists_and_permissions():
    assert os.path.isdir(SUPPORT_DIR), (
        f"Required directory {SUPPORT_DIR} is missing or not a directory."
    )
    mode = _mode_bits(SUPPORT_DIR)
    assert mode <= DIR_MODE, (
        f"Directory {SUPPORT_DIR} has permissions {oct(mode)}, "
        f"expected ≤ {oct(DIR_MODE)} for security."
    )


def test_logs_directory_exists_and_permissions():
    assert os.path.isdir(LOGS_DIR), (
        f"Required directory {LOGS_DIR} is missing or not a directory."
    )
    mode = _mode_bits(LOGS_DIR)
    assert mode <= DIR_MODE, (
        f"Directory {LOGS_DIR} has permissions {oct(mode)}, "
        f"expected ≤ {oct(DIR_MODE)}."
    )


def test_app_log_exists_permissions_and_contents():
    assert os.path.isfile(APP_LOG), (
        f"Log file {APP_LOG} is missing."
    )
    mode = _mode_bits(APP_LOG)
    assert mode <= FILE_MODE, (
        f"File {APP_LOG} has permissions {oct(mode)}, expected ≤ {oct(FILE_MODE)}."
    )

    with open(APP_LOG, "rt", encoding="utf-8") as fh:
        lines = fh.read().splitlines()

    assert lines == EXPECTED_APPLOG_LINES, dedent(
        f"""
        The contents of {APP_LOG} do not match the expected initial log.
        Expected lines ({len(EXPECTED_APPLOG_LINES)}):
        {EXPECTED_APPLOG_LINES}
        Found lines ({len(lines)}):
        {lines}
        """
    )


def test_diagnostics_directory_does_not_exist_yet():
    assert not os.path.exists(DIAG_DIR), (
        f"Directory {DIAG_DIR} should NOT exist before the student runs their solution."
    )


def test_output_files_do_not_exist_yet():
    for path in (ERRORS_LOG, COLLECTION_LOG):
        assert not os.path.exists(path), (
            f"Output file {path} should NOT exist before the student runs their solution."
        )