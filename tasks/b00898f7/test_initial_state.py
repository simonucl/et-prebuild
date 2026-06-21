# test_initial_state.py
#
# Pytest suite that validates the *initial* filesystem state
# before the student executes any shell commands.
#
# The expected layout is:
#   /home/user/db/                       --> must exist and be a directory
#   /home/user/db/improved_query.sql     --> must exist, be a file, and be non-empty
#   /home/user/db/archive_optimized_queries/  --> must NOT exist yet
#   /home/user/db/move.log               --> may be absent; if present, it must be 0-bytes
#
# Nothing else is verified or required at this stage.

import os
import pytest

DB_DIR = "/home/user/db"
IMPROVED_QUERY = os.path.join(DB_DIR, "improved_query.sql")
ARCHIVE_DIR = os.path.join(DB_DIR, "archive_optimized_queries")
MOVE_LOG = os.path.join(DB_DIR, "move.log")


def test_db_directory_exists():
    assert os.path.isdir(DB_DIR), (
        f"Required directory {DB_DIR} is missing or not a directory."
    )


def test_improved_query_exists_and_is_non_empty():
    assert os.path.isfile(IMPROVED_QUERY), (
        f"Required file {IMPROVED_QUERY} is missing."
    )
    size = os.path.getsize(IMPROVED_QUERY)
    assert size > 0, (
        f"File {IMPROVED_QUERY} should be non-empty, but its size is {size} bytes."
    )


def test_archive_directory_does_not_exist_yet():
    assert not os.path.exists(ARCHIVE_DIR), (
        f"Directory {ARCHIVE_DIR} should NOT exist before the task is started."
    )


def test_move_log_absent_or_empty():
    """
    move.log is allowed to be absent. If it exists, it must be an empty file
    so the student can append the first log line.
    """
    if not os.path.exists(MOVE_LOG):
        pytest.skip(f"{MOVE_LOG} does not exist yet (this is acceptable).")

    # If the file exists, ensure it is a regular file and 0 bytes long.
    assert os.path.isfile(MOVE_LOG), f"{MOVE_LOG} exists but is not a regular file."
    size = os.path.getsize(MOVE_LOG)
    assert size == 0, (
        f"{MOVE_LOG} should be empty (0 bytes) before the task starts, "
        f"but it is {size} bytes long."
    )


def test_improved_query_not_already_in_archive():
    archived_file = os.path.join(ARCHIVE_DIR, "improved_query.sql")
    assert not os.path.exists(archived_file), (
        f"{archived_file} should NOT exist before the move operation is performed."
    )