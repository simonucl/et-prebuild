# test_initial_state.py
#
# This test-suite validates the *initial* filesystem state **before**
# the student replaces the backup image with a hard-link.
#
# Expected starting conditions:
# 1. Two byte-for-byte identical files exist:
#       /home/user/images/primary/golden.img
#       /home/user/images/backup/golden.img
# 2. The two files have *different* inode numbers (they are separate copies).
# 3. Each file is exactly 256 KiB (262 144 bytes).
# 4. Neither file is a symbolic link.
#
# These assertions guarantee that the optimization step has real work to
# perform and that no output artefacts are pre-populated.

import os
import stat
import pytest

PRIMARY_PATH = "/home/user/images/primary/golden.img"
BACKUP_PATH = "/home/user/images/backup/golden.img"
PRIMARY_DIR = "/home/user/images/primary"
BACKUP_DIR = "/home/user/images/backup"
IMAGE_SIZE = 256 * 1024  # 256 KiB in bytes


def _assert_regular_file(path: str):
    """Helper: assert that path exists and is a regular file (not a symlink)."""
    assert os.path.exists(path), f"Expected file {path!r} to exist."
    assert os.path.isfile(path), f"Expected {path!r} to be a file."
    assert not os.path.islink(path), f"{path!r} should be a regular file, not a symlink."
    mode = os.stat(path, follow_symlinks=False).st_mode
    assert stat.S_ISREG(mode), f"{path!r} is not a regular file."


def test_directories_exist():
    """Primary and backup directories must exist."""
    for directory in (PRIMARY_DIR, BACKUP_DIR):
        assert os.path.isdir(directory), f"Required directory {directory!r} is missing."


def test_primary_file_exists_and_is_regular():
    _assert_regular_file(PRIMARY_PATH)


def test_backup_file_exists_and_is_regular():
    _assert_regular_file(BACKUP_PATH)


def test_files_are_identical_in_content():
    """Verify that both files contain exactly the same bytes."""
    with open(PRIMARY_PATH, "rb") as f_primary, open(BACKUP_PATH, "rb") as f_backup:
        content_primary = f_primary.read()
        content_backup = f_backup.read()

    assert content_primary == content_backup, (
        "Primary and backup image files differ in content; they should be exact copies."
    )


def test_files_are_expected_size():
    """Each image file must be exactly 256 KiB."""
    for path in (PRIMARY_PATH, BACKUP_PATH):
        size = os.path.getsize(path)
        assert size == IMAGE_SIZE, (
            f"{path!r} has size {size} bytes, expected {IMAGE_SIZE} bytes (256 KiB)."
        )


def test_files_have_different_inodes_initially():
    """
    Before optimization, the primary and backup files should be *different* physical
    copies, i.e., they must not share the same inode.
    """
    inode_primary = os.stat(PRIMARY_PATH, follow_symlinks=False).st_ino
    inode_backup = os.stat(BACKUP_PATH, follow_symlinks=False).st_ino
    assert inode_primary != inode_backup, (
        "Initial state invalid: primary and backup files already share an inode. "
        "They should be separate copies before optimization begins."
    )