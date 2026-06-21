# test_initial_state.py
#
# This pytest file validates the initial operating-system / filesystem state
# *before* the student carries out any actions.  It purposefully checks only the
# resources that are guaranteed to exist at the starting point of the exercise
# and avoids inspecting any of the outputs the student is asked to create.

import os
import stat
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# Constant reference data                                                     #
# --------------------------------------------------------------------------- #

LOG_DIR = Path("/home/user/logs")
LOG_PATH = LOG_DIR / "server.log"

EXPECTED_LOG_CONTENT = (
    "2023-11-25 10:01:02 INFO User logged in\n"
    "2023-11-25 10:02:15 ERROR 500 Internal Server Error at /login\n"
    "2023-11-25 10:03:47 WARN Disk space low\n"
    "2023-11-25 10:04:01 ERROR 404 Page Not Found /favicon.ico\n"
    "2023-11-25 10:05:19 ERROR 500 Internal Server Error at /api/data\n"
    "2023-11-25 10:06:33 ERROR 503 Service Unavailable at /reports\n"
    "2023-11-25 10:07:45 INFO Job completed\n"
    "2023-11-25 10:08:59 ERROR 500 Internal Server Error at /dashboard\n"
    "2023-11-25 10:09:14 ERROR 503 Service Unavailable at /login\n"
    "2023-11-25 10:10:21 ERROR 404 Page Not Found /robots.txt\n"
    "2023-11-25 10:12:30 ERROR 502 Bad Gateway at /metrics\n"
)

EXPECTED_LOG_LINES = EXPECTED_LOG_CONTENT.count("\n")  # 11 lines


# --------------------------------------------------------------------------- #
# Helper functions                                                            #
# --------------------------------------------------------------------------- #

def _mode(path: Path) -> int:
    """Return the permission bits of a filesystem object (e.g. 0o755)."""
    return stat.S_IMODE(path.stat().st_mode)


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #

def test_logs_directory_exists_and_has_correct_permissions():
    assert LOG_DIR.exists(), f"Expected directory {LOG_DIR} to exist."
    assert LOG_DIR.is_dir(), f"{LOG_DIR} exists but is not a directory."
    expected_perm = 0o755
    actual_perm = _mode(LOG_DIR)
    assert actual_perm == expected_perm, (
        f"{LOG_DIR} permissions should be {oct(expected_perm)}, "
        f"but are {oct(actual_perm)}."
    )


def test_server_log_file_exists_with_correct_permissions_and_content():
    # -------- existence & permissions --------------------------------------
    assert LOG_PATH.exists(), f"Expected file {LOG_PATH} to exist."
    assert LOG_PATH.is_file(), f"{LOG_PATH} exists but is not a regular file."
    expected_perm = 0o644
    actual_perm = _mode(LOG_PATH)
    assert actual_perm == expected_perm, (
        f"{LOG_PATH} permissions should be {oct(expected_perm)}, "
        f"but are {oct(actual_perm)}."
    )

    # -------- content -------------------------------------------------------
    content = LOG_PATH.read_text(encoding="utf-8")
    # Direct equality check ensures correct ordering, exact bytes, and the
    # presence of the final trailing newline.
    assert content == EXPECTED_LOG_CONTENT, (
        "The content of server.log does not match the expected initial state. "
        "If you have already modified the log, roll back to the provided copy."
    )

    # As an extra guard, verify line count matches the spec.
    line_count = content.count("\n")
    assert (
        line_count == EXPECTED_LOG_LINES
    ), f"Expected {EXPECTED_LOG_LINES} lines but found {line_count} lines in {LOG_PATH}."