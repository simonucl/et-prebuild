# test_initial_state.py
#
# This pytest suite validates the *initial* state of the operating system /
# filesystem **before** the student performs any actions.
#
# It makes sure that the expected backup source directory is present with the
# correct permissions and that the reference checksum manifest contains the
# exact two lines specified in the task description.
#
# NOTE:
# • Per the grading-suite instructions, we purposely do *not* test for the
#   presence or absence of any *output* directory or file (e.g.
#   /home/user/backup_audit or backup_integrity_report.log).  Those belong to
#   the *post-task* state and are therefore out of scope here.
# • Only the Python standard library + pytest are used.

import os
import stat
import hashlib
import pytest
from pathlib import Path

# Constant paths
HOME = Path("/home/user")
BACKUPS_DIR = HOME / "backups"
SHA256_FILE = BACKUPS_DIR / "sha256sums.txt"
DB_FILE = BACKUPS_DIR / "db.sql"
PHOTOS_FILE = BACKUPS_DIR / "photos.tar.gz"

# Expected constants
EMPTY_FILE_SHA256 = (
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
)  # correct SHA-256 of an empty file
WRONG_PHOTO_HASH = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
EXPECTED_MANIFEST_LINES = [
    f"{EMPTY_FILE_SHA256}  db.sql\n",
    f"{WRONG_PHOTO_HASH}  photos.tar.gz\n",
]


def _mode(path: Path) -> int:
    """
    Return the file permission bits (e.g. 0o755) of 'path' without the file type.
    """
    return stat.S_IMODE(path.stat().st_mode)


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_backups_directory_exists_and_permissions():
    assert BACKUPS_DIR.is_dir(), (
        f"Required directory {BACKUPS_DIR} is missing. "
        "The backup set must already exist before the task begins."
    )

    expected_mode = 0o777
    actual_mode = _mode(BACKUPS_DIR)
    assert (
        actual_mode == expected_mode
    ), f"{BACKUPS_DIR} should have permissions {oct(expected_mode)}, got {oct(actual_mode)}."


@pytest.mark.parametrize(
    "file_path",
    [DB_FILE, PHOTOS_FILE],
    ids=lambda p: str(p),
)
def test_backup_files_exist_and_are_empty(file_path: Path):
    assert file_path.is_file(), f"Expected file {file_path} is missing."

    size = file_path.stat().st_size
    assert size == 0, f"File {file_path} should be empty (0 bytes), got {size} bytes."


def test_sha256sums_file_exists_and_permissions():
    assert SHA256_FILE.is_file(), f"Checksum manifest {SHA256_FILE} is missing."

    expected_mode = 0o666
    actual_mode = _mode(SHA256_FILE)
    assert (
        actual_mode == expected_mode
    ), f"{SHA256_FILE} should have permissions {oct(expected_mode)}, got {oct(actual_mode)}."


def test_sha256sums_content_exact():
    with SHA256_FILE.open("r", encoding="utf-8") as f:
        content = f.readlines()

    assert (
        content == EXPECTED_MANIFEST_LINES
    ), (
        f"Contents of {SHA256_FILE} do not match the expected manifest.\n"
        f"Expected lines:\n{''.join(EXPECTED_MANIFEST_LINES)}\n"
        f"Actual lines:\n{''.join(content)}"
    )


def test_empty_file_hash_in_manifest_is_correct():
    """
    Sanity check: compute the SHA-256 hash of /home/user/backups/db.sql and
    confirm that it matches the corresponding entry in sha256sums.txt.  This
    guards against silent data corruption in the test environment itself.
    """
    hasher = hashlib.sha256()
    with DB_FILE.open("rb") as f:
        hasher.update(f.read())
    actual_hash = hasher.hexdigest()

    assert (
        actual_hash == EMPTY_FILE_SHA256
    ), f"SHA-256 of {DB_FILE} should be {EMPTY_FILE_SHA256}, got {actual_hash}."