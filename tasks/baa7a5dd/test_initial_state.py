# test_initial_state.py
"""
Pytest suite to verify the **initial** operating-system / filesystem state
_before_ the student performs any actions for the database-migration task.

Everything that the student is supposed to create **must be absent** so the
exercise starts from a clean slate.
"""

from pathlib import Path
import pytest

HOME = Path("/home/user")
DB_DIR = HOME / "databases"
LOG_DIR = HOME / "migration_logs"
OLD_DB = DB_DIR / "old_db.sqlite"
NEW_DB = DB_DIR / "new_db.sqlite"
LOG_FILE = LOG_DIR / "validation_results.log"


def _assert_absent(path: Path):
    """
    Helper: assert that the given path does not exist in the file-system.
    Produces a clear message if the path is unexpectedly present.
    """
    assert not path.exists(), f"Path should NOT exist yet: {path}"


def test_home_directory_exists():
    """
    Sanity check: the base home directory for the student must exist.
    """
    assert HOME.exists() and HOME.is_dir(), (
        "Expected base directory /home/user to exist, but it is missing. "
        "The testing environment is misconfigured."
    )


@pytest.mark.parametrize(
    "path",
    [
        DB_DIR,
        LOG_DIR,
    ],
)
def test_expected_directories_absent(path):
    """
    Directories that the student must create should not be present yet.
    """
    _assert_absent(path)


@pytest.mark.parametrize(
    "path",
    [
        OLD_DB,
        NEW_DB,
        LOG_FILE,
    ],
)
def test_expected_files_absent(path):
    """
    SQLite databases and the validation log file must not exist prior
    to the student's work.
    """
    _assert_absent(path)