# test_initial_state.py
#
# This test-suite validates the *initial* filesystem state **before**
# the student’s backup/restore script is executed.  The assertions are
# intentionally strict so that any pre-existing artefacts immediately
# surface as test failures with an explanatory message.
#
# Allowed libraries: stdlib + pytest only.

import os
from pathlib import Path
import pytest
import stat

HOME = Path("/home/user")
BACKUPS_DIR = HOME / "backups"
TEST_DATA_DIR = HOME / "test_data"

# ---------------------------------------------------------------------- 
# Helper utilities
# ---------------------------------------------------------------------- 

def _is_writable_directory(path: Path) -> bool:
    """
    Return True if `path` is an existing directory that the current user can
    create files in.  We attempt `os.access` with W_OK and also check the
    execute bit so entering the directory works.
    """
    return (
        path.is_dir()
        and os.access(path, os.W_OK | os.X_OK)
    )

# ---------------------------------------------------------------------- 
# Tests for the presence of required *base* directories
# ---------------------------------------------------------------------- 

def test_home_directory_exists():
    assert HOME.is_dir(), (
        f"Expected base directory {HOME} to exist before the exercise starts."
    )

def test_backups_directory_exists_and_is_writable():
    assert BACKUPS_DIR.is_dir(), (
        f"Directory {BACKUPS_DIR} must exist before the exercise starts."
    )
    assert _is_writable_directory(BACKUPS_DIR), (
        f"Directory {BACKUPS_DIR} exists but is not writable/executable "
        f"for the current user.  Please ensure correct permissions."
    )

# ---------------------------------------------------------------------- 
# Tests that *no* artefacts from the yet-to-be-performed task exist
# ---------------------------------------------------------------------- 

# Paths that must NOT exist at the very beginning.
NON_EXISTENT_PATHS = [
    TEST_DATA_DIR / "project_omega",
    TEST_DATA_DIR / "project_sigma",
    BACKUPS_DIR / "project_omega_backup.tar.gz",
    BACKUPS_DIR / "project_sigma_backup.tar.gz",
    HOME / "restore_benchmark.log",
]

@pytest.mark.parametrize("path", NON_EXISTENT_PATHS)
def test_no_preexisting_task_artefacts(path: Path):
    assert not path.exists(), (
        f"Path {path} should NOT exist before the student runs their script. "
        f"Found an unexpected file/directory which would invalidate the "
        f"initial test conditions."
    )

# ---------------------------------------------------------------------- 
# Optional: if /home/user/test_data exists, ensure it contains no project_* dirs
# ---------------------------------------------------------------------- 

def test_test_data_directory_clean():
    """
    /home/user/test_data/ may or may not exist initially.  If it does, it must
    *not* already contain project_omega or project_sigma directories.
    """
    if TEST_DATA_DIR.exists():
        assert TEST_DATA_DIR.is_dir(), (
            f"{TEST_DATA_DIR} exists but is not a directory."
        )
        forbidden = {"project_omega", "project_sigma"}
        present = {p.name for p in TEST_DATA_DIR.iterdir() if p.is_dir()}
        unexpected = forbidden & present
        assert not unexpected, (
            f"The following dataset directories must NOT pre-exist in "
            f"{TEST_DATA_DIR}: {', '.join(sorted(unexpected))}"
        )