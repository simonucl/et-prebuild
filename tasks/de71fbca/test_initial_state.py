# test_initial_state.py
#
# This test-suite asserts the **initial** state of the work-station,
# i.e. before the student has created any artefacts for the exercise.
#
# Expectations BEFORE the student’s work starts:
#   1. The SQLite CLI tool `sqlite3` must be available in $PATH.
#   2. The files that the student is supposed to create
#        /home/user/build_stats.db
#        /home/user/build_report.txt
#      must NOT exist yet.
#
# If any of these assertions fail, the exercise environment is in an
# unexpected state and should be reset before grading the student’s
# submission.

import os
import shutil
from pathlib import Path
import pytest

HOME = Path("/home/user")
DB_PATH = HOME / "build_stats.db"
REPORT_PATH = HOME / "build_report.txt"


def test_sqlite_cli_is_available():
    """
    The stock `sqlite3` command-line client must be present in PATH so that
    the student can use it to create the database.  We do *not* check
    exact version, only that the executable can be resolved.
    """
    sqlite_path = shutil.which("sqlite3")
    assert sqlite_path is not None, (
        "sqlite3 executable not found in PATH. "
        "It is required for the exercise."
    )
    # Extra sanity check: the resolved path really points to an executable file
    assert os.access(sqlite_path, os.X_OK), (
        f"Resolved sqlite3 at '{sqlite_path}', but it is not executable."
    )


@pytest.mark.parametrize(
    "target_path,description",
    [
        (DB_PATH, "SQLite database '/home/user/build_stats.db'"),
        (REPORT_PATH, "Report file '/home/user/build_report.txt'"),
    ],
)
def test_deliverable_files_do_not_exist_yet(target_path: Path, description: str):
    """
    Before the student starts, none of the expected deliverable files should
    exist.  Their presence would indicate that the environment is not clean
    or that a previous run spilled artefacts into the workspace.
    """
    assert not target_path.exists(), (
        f"{description} already exists. The workspace must be clean before "
        f"the student runs their solution."
    )