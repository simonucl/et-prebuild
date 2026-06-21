# test_initial_state.py
#
# Pytest suite to verify that the system is in a **clean** state
# before the student begins the “tiny local database” task.
#
# These tests PASS when none of the required end-state artefacts
# (directory, SQLite DB, CSV, or log file) are present yet.
#
# If any artefact already exists, the corresponding test will FAIL
# with a clear, actionable message.

import os
import pytest

# Base paths that must NOT exist at the very beginning of the task
DIR_PATH = "/home/user/projects/db_task"
DB_PATH = "/home/user/projects/db_task/myapp.db"
CSV_PATH = "/home/user/projects/db_task/users_export.csv"
LOG_PATH = "/home/user/projects/db_task/db_operations.log"


@pytest.mark.parametrize(
    "path, kind",
    [
        (DIR_PATH, "directory"),
        (DB_PATH, "file"),
        (CSV_PATH, "file"),
        (LOG_PATH, "file"),
    ],
)
def test_required_artefacts_absent(path: str, kind: str) -> None:
    """
    Ensure that none of the deliverable artefacts exist
    before the student starts working on the assignment.
    """
    exists = os.path.exists(path)
    assert not exists, (
        f"The {kind} '{path}' already exists, but the initial state should be empty. "
        f"Please remove it before beginning the task."
    )