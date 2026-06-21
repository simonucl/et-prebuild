# test_initial_state.py
#
# This pytest suite validates the *initial* state of the operating system /
# filesystem before the learner performs any action.  If any of these tests
# fail, the learner is starting from an unexpected environment.

import os
import stat
import pytest

HOME = "/home/user"
BASE_DIR = os.path.join(HOME, "cloud_migration")
ALERTS_DIR = os.path.join(BASE_DIR, "alerts")
LOG_FILE = os.path.join(BASE_DIR, "full_system.log")

# --------------------------------------------------------------------------- #
# Expected content of full_system.log (including the single trailing newline)
# --------------------------------------------------------------------------- #
EXPECTED_LOG_CONTENT = (
    "[2023-10-01 08:10:16] [INFO] [auth-service] User login successful userId=23\n"
    "[2023-10-01 08:10:18] [WARN] [gateway] High latency detected route=/api/payments\n"
    "[2023-10-01 08:10:20] [ERROR] [db-service] Connection timeout to primary replica\n"
    "[2023-10-01 08:11:05] [INFO] [billing-service] Invoice generated invoiceId=9821\n"
    "[2023-10-01 08:12:45] [CRITICAL] [db-service] Data corruption detected segment=alpha\n"
    "[2023-10-01 08:13:02] [ERROR] [cache-service] Redis cluster unreachable\n"
    "[2023-10-01 08:14:33] [INFO] [db-service] Background vacuum completed table=orders\n"
    "[2023-10-01 08:15:14] [WARN] [auth-service] Suspicious login attempt userId=88\n"
    "[2023-10-01 08:16:29] [ERROR] [db-service] Failed to apply migration file V23__add_index.sql\n"
    "[2023-10-01 08:17:42] [INFO] [gateway] Deployment finished version=1.3.4\n"
)


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def is_writable(path: str) -> bool:
    """
    Return True if the current user can create a file in `path`.
    """
    return os.access(path, os.W_OK)


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_base_directory_exists_and_writable():
    assert os.path.isdir(
        BASE_DIR
    ), f"Required directory {BASE_DIR!r} does not exist or is not a directory."
    assert is_writable(
        BASE_DIR
    ), f"Directory {BASE_DIR!r} is not writable by the current user."


def test_alerts_directory_absent():
    assert not os.path.exists(
        ALERTS_DIR
    ), f"Directory {ALERTS_DIR!r} should NOT exist before the task is started."


def test_log_file_exists_with_correct_content():
    assert os.path.isfile(
        LOG_FILE
    ), f"Required log file {LOG_FILE!r} does not exist."

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        data = f.read()

    # Content must match *exactly* (including trailing newline)
    assert (
        data == EXPECTED_LOG_CONTENT
    ), (
        f"Content of {LOG_FILE!r} does not match the expected initial fixture.\n"
        "If you modified this file, restore it to the original 10-line version "
        "provided in the task description."
    )

    # Additional sanity: ensure exactly 10 lines
    lines = data.splitlines()
    assert len(lines) == 10, (
        f"{LOG_FILE!r} should contain exactly 10 lines, "
        f"but {len(lines)} lines were found."
    )


def test_solution_output_files_do_not_exist_yet():
    """
    Before the learner runs their solution, no output files or directories
    should exist inside `alerts/`.
    """
    for fname in (
        "critical_db.log",
        "critical_db_summary.txt",
    ):
        path = os.path.join(ALERTS_DIR, fname)
        assert not os.path.exists(
            path
        ), f"Output file {path!r} should NOT exist before the learner's solution runs."