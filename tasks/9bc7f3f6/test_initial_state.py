# test_initial_state.py
#
# This test-suite is executed *before* the student starts working.
# It asserts that none of the artefacts that must be created by the
# student already exist.  A clean slate guarantees that the grading
# tests can later attribute every new file, directory and database
# object exclusively to the student’s commands.
#
# The tests purposefully **fail** if any of the target paths already
# exist or if `sqlite3` is not available in the PATH, because those
# conditions would invalidate the exercise setup.

import shutil
import subprocess
from pathlib import Path

import pytest

# Canonical paths used throughout the assignment
HOME = Path("/home/user")
ROOT_DIR = HOME / "experiments" / "sqlite_demo"
DB_FILE = ROOT_DIR / "experiment_tracking.db"
LOG_FILE = ROOT_DIR / "experiment_report.log"


def _repr_path(p: Path) -> str:
    """Return a platform-neutral string representation of a path."""
    return str(p)


def test_sqlite3_cli_is_available():
    """
    sqlite3 must be present on the system before the student starts working.
    The test looks the executable up in the current PATH.
    """
    sqlite3_path = shutil.which("sqlite3")
    assert (
        sqlite3_path is not None
    ), "sqlite3 CLI executable is not available in PATH; it is required for the exercise."


def test_root_directory_does_not_exist_yet():
    """
    The directory /home/user/experiments/sqlite_demo must NOT exist prior to
    the student's commands.  Its creation is part of the assignment.
    """
    assert (
        not ROOT_DIR.exists()
    ), f"Directory {_repr_path(ROOT_DIR)} already exists, but it should be created by the student."


@pytest.mark.parametrize(
    "path_obj, description",
    [
        (DB_FILE, "SQLite database file"),
        (LOG_FILE, "log file experiment_report.log"),
    ],
)
def test_no_preexisting_files(path_obj: Path, description: str):
    """
    Neither the database nor the log file should exist yet.
    """
    assert (
        not path_obj.exists()
    ), f"{description} {_repr_path(path_obj)} already exists; the student must create it during the exercise."


def test_parent_directory_state():
    """
    The parent directory /home/user/experiments may or may not exist.
    If it exists, it must NOT already contain a subdirectory named 'sqlite_demo'.
    This is a redundant guard to catch cases where an empty directory was
    inadvertently created.
    """
    parent = ROOT_DIR.parent
    if parent.exists():
        assert (
            "sqlite_demo" not in [p.name for p in parent.iterdir()]
        ), f"The parent directory {_repr_path(parent)} already contains a child called 'sqlite_demo'; it should not exist yet."