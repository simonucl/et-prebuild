# test_initial_state.py
"""
Pytest suite that verifies the *initial* operating-system / filesystem
state, i.e. _before_ the learner carries out any work on the task.

The task eventually expects the following artefacts to be CREATED inside
/home/user:

    /home/user/build
    /home/user/build/reports
    /home/user/build/logs
    /home/user/build/artifacts_store.db
    /home/user/build/reports/latest_build_artifacts.csv
    /home/user/build/logs/db_operations.log

Therefore, at the very beginning none of the above must exist.
The tests below assert exactly that and will **fail** if any of these
paths are already present, signalling that the environment is not clean.

Only the standard library and pytest are used.
"""
import os
import stat
import shutil
import pytest
from pathlib import Path

HOME = Path("/home/user").resolve()

# Paths that must NOT exist at the start of the exercise
EXPECTED_FRESH_PATHS = [
    HOME / "build",
    HOME / "build" / "reports",
    HOME / "build" / "logs",
    HOME / "build" / "artifacts_store.db",
    HOME / "build" / "reports" / "latest_build_artifacts.csv",
    HOME / "build" / "logs" / "db_operations.log",
]


def _human(path: Path) -> str:
    """Return a human-readable absolute path string."""
    return str(path)


def test_home_directory_exists_and_is_writable():
    assert HOME.exists(), f"Expected home directory {_human(HOME)} to exist."
    assert HOME.is_dir(), f"{_human(HOME)} exists but is not a directory."
    # Check write permission for the current (non-root) user
    mode = HOME.stat().st_mode
    writable = bool(mode & stat.S_IWUSR)
    assert writable, f"Home directory {_human(HOME)} should be writable by the user."


@pytest.mark.parametrize("path", EXPECTED_FRESH_PATHS)
def test_expected_artifacts_absent_initially(path: Path):
    assert not path.exists(), (
        f"The path {_human(path)} already exists, but the exercise requires "
        f"students to create it. Ensure the initial environment is clean."
    )


def test_sqlite3_cli_is_available():
    """
    The instructions mandate using the `sqlite3` CLI tool.  It does not have
    to be on $PATH *yet* for the student, but it must at least be installed
    on the system so the learner can invoke it.

    We therefore only check that `shutil.which` can locate it.
    """
    sqlite_path = shutil.which("sqlite3")
    assert sqlite_path, (
        "sqlite3 command-line client not found in PATH. "
        "It is required for the student to complete the task."
    )