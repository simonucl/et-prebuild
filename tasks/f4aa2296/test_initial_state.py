# test_initial_state.py
"""
Pytest suite that validates the **initial** state of the operating-system /
filesystem **before** the student performs any action.

If any test in this file fails, it means the playground is not in the expected
starting condition and the student will be unable to complete the exercise as
specified.
"""

import os
import stat
from pathlib import Path

# --------------------------------------------------------------------------- #
# Constants – absolute, canonical paths only                                  #
# --------------------------------------------------------------------------- #
HOME = Path("/home/user").resolve()

REMOTE_ROOT = HOME / "remote_host_sim"
REMOTE_APP_LOGS = REMOTE_ROOT / "app_logs"

LOCAL_ROOT = HOME / "local_backup"
LOCAL_APP_LOGS = LOCAL_ROOT / "app_logs"

SYNC_REPORTS_DIR = HOME / "sync_reports"
EXPECTED_REPORT = SYNC_REPORTS_DIR / "2023-10-05_rsync_report.txt"

REMOTE_FILES = {
    "app-2023-10-01.log": "LOG-A\n",
    "app-2023-10-02.log": "LOG-B\n",
    "debug-2023-10-01.log": "DEBUG-A\n",
    "session.tmp": "TEMP\n",
}

# --------------------------------------------------------------------------- #
# Helper utilities                                                            #
# --------------------------------------------------------------------------- #
def _octal_perm(path: Path) -> str:
    """Return the permission bits of *path* as a string such as '755'."""
    return oct(path.stat().st_mode & 0o777)[-3:]


def _assert_dir(path: Path, *, should_exist: bool = True, perm: str = "755"):
    """Assert directory existence and permissions."""
    if should_exist:
        assert path.is_dir(), f"Directory {path} should exist and be a directory."
        assert _octal_perm(path) == perm, (
            f"Directory {path} should have permissions {perm}, "
            f"found {_octal_perm(path)}"
        )
    else:
        assert not path.exists(), f"Directory {path} must NOT exist initially."


def _assert_file(path: Path, *, should_exist: bool = True, perm: str = "644"):
    """Assert file existence and permissions."""
    if should_exist:
        assert path.is_file(), f"File {path} should exist."
        assert _octal_perm(path) == perm, (
            f"File {path} should have permissions {perm}, "
            f"found {_octal_perm(path)}"
        )
    else:
        assert not path.exists(), f"File {path} must NOT exist initially."


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #
def test_required_directories_exist_with_correct_permissions():
    """Remote and local directories must pre-exist with 755 perms."""
    _assert_dir(REMOTE_ROOT)
    _assert_dir(REMOTE_APP_LOGS)
    _assert_dir(LOCAL_ROOT)
    _assert_dir(LOCAL_APP_LOGS)

def test_sync_reports_directory_must_not_exist():
    """The reports directory should NOT exist before the task starts."""
    _assert_dir(SYNC_REPORTS_DIR, should_exist=False)

def test_remote_log_files_and_their_contents():
    """
    The remote directory must contain exactly the four expected files
    with the specified byte contents.
    """
    actual_files = sorted(p.name for p in REMOTE_APP_LOGS.iterdir() if p.is_file())
    expected_files = sorted(REMOTE_FILES.keys())
    assert actual_files == expected_files, (
        f"Remote directory {REMOTE_APP_LOGS} should contain exactly "
        f"{expected_files}. Found {actual_files}"
    )

    # Verify file contents
    for filename, expected_content in REMOTE_FILES.items():
        file_path = REMOTE_APP_LOGS / filename
        _assert_file(file_path)
        with file_path.open("r", encoding="utf-8") as fh:
            content = fh.read()
        assert (
            content == expected_content
        ), f"File {file_path} has unexpected content. Expected {expected_content!r}, got {content!r}"

def test_local_backup_directory_is_initially_empty():
    """
    The local backup directory must exist but contain **no** files
    before synchronisation occurs.
    """
    assert LOCAL_APP_LOGS.is_dir(), f"{LOCAL_APP_LOGS} should already exist."
    files_present = [p.name for p in LOCAL_APP_LOGS.iterdir() if p.is_file()]
    assert files_present == [], (
        f"Local backup directory {LOCAL_APP_LOGS} should be empty initially; "
        f"found files: {files_present}"
    )

def test_report_file_does_not_exist_yet():
    """The rsync report must not pre-exist before the student generates it."""
    _assert_file(EXPECTED_REPORT, should_exist=False)