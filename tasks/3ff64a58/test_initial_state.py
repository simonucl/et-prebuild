# test_initial_state.py
"""
Pytest suite that verifies the **initial** filesystem state before the
student performs any action for the “tidy-up PostgreSQL dump area” task.

This test file checks that:
1. The expected directories exist.
2. The four compressed dump files are present in /home/user/db_archives/.
3. The two *obsolete* symbolic links exist in /home/user/db_backups/ and
   still point to the **20230918** files.
4. There is **no** update_symlinks.log file yet.

If any assertion fails, the accompanying message should make it clear
what is missing or incorrect.
"""

import os
from pathlib import Path
import pytest

# --- Constants ----------------------------------------------------------------

HOME = Path("/home/user")
ARCHIVES_DIR = HOME / "db_archives"
BACKUPS_DIR = HOME / "db_backups"

ARCHIVE_FILES = {
    ARCHIVES_DIR / "prod_20230918.sql.gz",
    ARCHIVES_DIR / "prod_20230919.sql.gz",
    ARCHIVES_DIR / "stg_20230918.sql.gz",
    ARCHIVES_DIR / "stg_20230919.sql.gz",
}

EXPECTED_SYMLINKS = {
    BACKUPS_DIR / "latest_prod": ARCHIVES_DIR / "prod_20230918.sql.gz",
    BACKUPS_DIR / "latest_staging": ARCHIVES_DIR / "stg_20230918.sql.gz",
}

LOG_FILE = BACKUPS_DIR / "update_symlinks.log"

# ------------------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------------------

def _human(path: Path) -> str:
    """Return a human-readable version of a Path for error messages."""
    return str(path)


# ------------------------------------------------------------------------------
# Tests
# ------------------------------------------------------------------------------

def test_directories_exist():
    """Both /home/user/db_archives and /home/user/db_backups must exist."""
    assert ARCHIVES_DIR.is_dir(), f"Missing directory: {_human(ARCHIVES_DIR)}"
    assert BACKUPS_DIR.is_dir(), f"Missing directory: {_human(BACKUPS_DIR)}"


@pytest.mark.parametrize("file_path", sorted(ARCHIVE_FILES))
def test_archive_files_present(file_path: Path):
    """Each of the four compressed dump files must exist in the archives dir."""
    assert file_path.is_file(), f"Archive file missing: {_human(file_path)}"


@pytest.mark.parametrize("link_path, expected_target", EXPECTED_SYMLINKS.items())
def test_obsolete_symlinks_present_and_correct(link_path: Path, expected_target: Path):
    """
    The two *out-of-date* symlinks must exist and still point to the
    20230918 files before the student updates them.
    """
    assert link_path.exists(), f"Expected symlink missing: {_human(link_path)}"
    assert link_path.is_symlink(), f"{_human(link_path)} is not a symbolic link"

    actual_target = Path(os.readlink(link_path))
    assert actual_target == expected_target, (
        f"{_human(link_path)} points to {_human(actual_target)}, "
        f"but should point to {_human(expected_target)} in the initial state."
    )


def test_log_file_not_present_yet():
    """
    The log file must NOT exist at the start of the exercise.
    It will be created by the student's solution later.
    """
    assert not LOG_FILE.exists(), (
        f"Unexpected log file found at {_human(LOG_FILE)}; "
        "the initial state should not contain this file."
    )