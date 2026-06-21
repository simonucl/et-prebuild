# test_initial_state.py
#
# Pytest suite that validates the **initial** operating-system / filesystem
# state before the student creates the archive and checksum log.
#
# What we expect to ALREADY exist
#   /home/user/source_data/
#       ├── customer_list.csv      (92  bytes)
#       ├── inventory.json         (92  bytes)
#       ├── readme.txt             (120 bytes)
#       └── scripts/
#              └── cleanup.sh      (48  bytes)
#
# What we expect to **NOT** exist yet
#   /home/user/backups/nightly_20240315.tar.gz
#   /home/user/backups/nightly_20240315_checksums.log
#
# The “/home/user/backups” directory itself may or may not exist at this point;
# both are acceptable – the student’s instructions cover its creation.
#
# Only stdlib + pytest are used.

from pathlib import Path
import os
import pytest

SOURCE_ROOT = Path("/home/user/source_data")
BACKUP_DIR = Path("/home/user/backups")
ARCHIVE_PATH = BACKUP_DIR / "nightly_20240315.tar.gz"
LOG_PATH = BACKUP_DIR / "nightly_20240315_checksums.log"

# -----------------------------------------------------------------------------
# Tests for things that MUST exist
# -----------------------------------------------------------------------------

def test_source_data_root_exists_and_is_dir():
    assert SOURCE_ROOT.exists(), (
        f"Expected directory {SOURCE_ROOT} to exist but it is missing."
    )
    assert SOURCE_ROOT.is_dir(), (
        f"{SOURCE_ROOT} exists but is not a directory."
    )

@pytest.mark.parametrize(
    "relative_path,expected_size",
    [
        ("customer_list.csv", 92),
        ("inventory.json", 92),
        ("readme.txt", 120),
        ("scripts/cleanup.sh", 48),
    ],
)
def test_required_files_exist_with_correct_size(relative_path, expected_size):
    full_path = SOURCE_ROOT / relative_path
    assert full_path.exists(), (
        f"Required file {full_path} is missing."
    )
    assert full_path.is_file(), (
        f"Expected {full_path} to be a regular file."
    )
    actual_size = full_path.stat().st_size
    assert actual_size == expected_size, (
        f"{full_path} has size {actual_size} bytes, "
        f"but {expected_size} bytes were expected."
    )

def test_scripts_subdirectory_is_directory():
    scripts_dir = SOURCE_ROOT / "scripts"
    assert scripts_dir.exists(), (
        f"Expected subdirectory {scripts_dir} to exist but it is missing."
    )
    assert scripts_dir.is_dir(), (
        f"{scripts_dir} exists but is not a directory."
    )

# -----------------------------------------------------------------------------
# Tests for things that MUST NOT exist yet
# -----------------------------------------------------------------------------

def test_archive_and_log_do_not_exist_initially():
    """
    Before the student runs their solution there must be no pre-existing
    archive or checksum log.  Their task includes creating them.
    """
    assert not ARCHIVE_PATH.exists(), (
        f"Archive {ARCHIVE_PATH} already exists – it should *not* be present "
        f"before the task is performed."
    )
    assert not LOG_PATH.exists(), (
        f"Checksum log {LOG_PATH} already exists – it should *not* be present "
        f"before the task is performed."
    )