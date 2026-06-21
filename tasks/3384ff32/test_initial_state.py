# test_initial_state.py
#
# Pytest suite that verifies the **initial** filesystem state
# before the student updates the symlink and creates the log.
#
# Expected initial layout (all paths are absolute):
#
#   /home/user/db_backups/
#       backup_2023-07-01.sql.gz   (regular 0-byte file)
#       backup_2023-07-02.sql.gz   (regular 0-byte file)
#       backup_2023-07-03.sql.gz   (regular 0-byte file)
#       latest                     (symlink → backup_2023-07-02.sql.gz)
#
#   • The file link_update.log must NOT exist yet.
#
# Any deviation from the above will cause these tests to fail
# and inform the student that they are not starting from the
# required baseline.

import os
import stat
from pathlib import Path

BACKUP_DIR = Path("/home/user/db_backups")
BACKUP_FILES = [
    "backup_2023-07-01.sql.gz",
    "backup_2023-07-02.sql.gz",
    "backup_2023-07-03.sql.gz",
]
LATEST_SYMLINK = BACKUP_DIR / "latest"
LOG_FILE = BACKUP_DIR / "link_update.log"


def _assert_regular_zero_byte_file(path: Path):
    assert path.exists(), f"File missing: {path}"
    assert path.is_file() and not path.is_symlink(), f"{path} is not a regular file"
    size = path.stat().st_size
    assert size == 0, f"Expected {path} to be 0 bytes, got {size} bytes"


def test_backup_directory_exists():
    assert BACKUP_DIR.exists(), f"Directory missing: {BACKUP_DIR}"
    assert BACKUP_DIR.is_dir(), f"{BACKUP_DIR} is not a directory"


def test_all_backup_files_present_and_empty():
    for fname in BACKUP_FILES:
        _assert_regular_zero_byte_file(BACKUP_DIR / fname)


def test_latest_symlink_points_to_2023_07_02():
    assert LATEST_SYMLINK.exists(), f"Symlink missing: {LATEST_SYMLINK}"
    assert LATEST_SYMLINK.is_symlink(), f"{LATEST_SYMLINK} is not a symlink"

    # Resolve the symlink target to an absolute path for comparison.
    resolved_path = LATEST_SYMLINK.resolve()
    expected_path = (BACKUP_DIR / "backup_2023-07-02.sql.gz").resolve()

    assert (resolved_path == expected_path), (
        f"Symlink 'latest' points to {resolved_path}, "
        f"but expected it to point to {expected_path}"
    )


def test_link_update_log_does_not_exist_yet():
    assert not LOG_FILE.exists(), (
        f"{LOG_FILE} already exists; the log file should be created "
        "only after the symlink is updated."
    )