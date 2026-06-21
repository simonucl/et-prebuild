# test_initial_state.py
"""
Pytest suite that validates the REQUIRED **initial** operating-system /
filesystem state for the outbound-sync exercise, *before* the student
performs any action.

If any of these tests fail, the exercise environment is not in the
expected starting condition.
"""

import os
from pathlib import Path

# --------------------------------------------------------------------------- #
# CONSTANTS – full, absolute paths as required by the grading rules
# --------------------------------------------------------------------------- #
HOME = Path("/home/user")

WORKSPACE_DIR      = HOME / "workspace"
PROJECT_DIR        = WORKSPACE_DIR / "project"

EXCLUDE_FILE       = WORKSPACE_DIR / "sync-exclude.txt"

REMOTE_ROOT        = HOME / "remote_host"
REMOTE_BACKUP_DIR  = REMOTE_ROOT / "project_backup"

REPORTS_DIR        = HOME / "sync_reports"
SYNC_LOG_FILE      = REPORTS_DIR / "initial_sync.log"

# Source-project expected files
SRC_FILES = {
    PROJECT_DIR / "app.py",
    PROJECT_DIR / "config.yaml",
    PROJECT_DIR / "secrets.yaml",
    PROJECT_DIR / "notes.tmp",
    PROJECT_DIR / "README.md",
    PROJECT_DIR / "utils" / "helper.py",
}

# --------------------------------------------------------------------------- #
# HELPER ASSERTIONS
# --------------------------------------------------------------------------- #
def _assert_path_exists(path: Path, is_dir: bool | None = None) -> None:
    """
    Assert that *path* exists.  If *is_dir* is True, the path must be a
    directory; if False, it must be a regular file; if None, type is ignored.
    """
    assert path.exists(), f"Expected '{path}' to exist."
    if is_dir is True:
        assert path.is_dir(), f"Expected '{path}' to be a directory."
    elif is_dir is False:
        assert path.is_file(), f"Expected '{path}' to be a regular file."


# --------------------------------------------------------------------------- #
# TESTS
# --------------------------------------------------------------------------- #
def test_source_project_structure():
    """All required source files/directories must already exist."""
    _assert_path_exists(PROJECT_DIR, is_dir=True)

    # utils/ sub-directory
    utils_dir = PROJECT_DIR / "utils"
    _assert_path_exists(utils_dir, is_dir=True)

    # Individual files
    for file_path in SRC_FILES:
        _assert_path_exists(file_path, is_dir=False)


def test_exclude_file_not_yet_present():
    """The rsync exclude list should NOT yet exist before the student creates it."""
    assert not EXCLUDE_FILE.exists(), (
        "Exclude file '{EXCLUDE_FILE}' should NOT exist before the task is performed."
    )


def test_remote_backup_dir_exists_and_is_empty():
    """Backup directory exists but must be empty prior to first rsync run."""
    _assert_path_exists(REMOTE_BACKUP_DIR, is_dir=True)

    contents = list(REMOTE_BACKUP_DIR.iterdir())
    assert (
        len(contents) == 0
    ), f"Remote backup directory '{REMOTE_BACKUP_DIR}' is expected to be empty; found {len(contents)} item(s)."


def test_sync_log_not_yet_present():
    """No synchronisation log should exist before the student runs rsync."""
    # reports directory may or may not exist, but log file must not
    if SYNC_LOG_FILE.exists():
        pytest.fail(
            f"Log file '{SYNC_LOG_FILE}' should NOT exist before the task is performed."
        )


def test_no_unexpected_files_in_remote_backup():
    """Safety net: there must be no .tmp or secrets.yaml in the empty backup dir."""
    tmp_files = list(REMOTE_BACKUP_DIR.rglob("*.tmp"))
    secrets_files = list(REMOTE_BACKUP_DIR.rglob("secrets.yaml"))

    assert not tmp_files, (
        "Remote backup directory should be empty; found .tmp files: "
        + ", ".join(str(p) for p in tmp_files)
    )
    assert not secrets_files, (
        "Remote backup directory should be empty; found 'secrets.yaml' files."
    )