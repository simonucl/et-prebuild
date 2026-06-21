# test_initial_state.py
#
# Pytest suite that validates the INITIAL state of the operating-system
# before the student (“backupadmin”) begins to work on the weekly archive
# assignment.  The tests make sure the pre-existing data set under
# /home/user/data/ is exactly as described and that no archive artifacts
# are present yet.
#
# Requirements verified:
#   • Directory /home/user/data and its two sub-directories “raw” and
#     “reports” exist with mode 700.
#   • Three regular files exist with mode 600, the correct byte-sizes
#     and the exact reference contents/sha256 checksums.
#   • No directory /home/user/backup_archives (or any of its expected
#     output files) is present yet.

import os
import stat
import hashlib
import pytest


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

DATA_ROOT = "/home/user/data"
BACKUP_DIR = "/home/user/backup_archives"

EXPECTED_DIRS = {
    DATA_ROOT: 0o700,
    os.path.join(DATA_ROOT, "raw"): 0o700,
    os.path.join(DATA_ROOT, "reports"): 0o700,
}

# path         : (expected_size, expected_content)
EXPECTED_FILES = {
    os.path.join(DATA_ROOT, "raw", "file_a.txt"): (6, b"alpha\n"),
    os.path.join(DATA_ROOT, "raw", "file_b.txt"): (5, b"beta\n"),
    os.path.join(DATA_ROOT, "reports", "summary.txt"): (15, b"summary report\n"),
}


def _mode(path: str) -> int:
    """Return the permission bits (e.g. 0o700) of a filesystem object."""
    return stat.S_IMODE(os.stat(path).st_mode)


def _sha256(data: bytes) -> str:
    """Return SHA-256 hex digest of *data*."""
    return hashlib.sha256(data).hexdigest()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_directories_exist_and_have_correct_permissions():
    """
    Verify that /home/user/data, /raw and /reports directories exist
    and have mode 700 (rwx------).
    """
    for dpath, expected_mode in EXPECTED_DIRS.items():
        assert os.path.isdir(dpath), f"Required directory {dpath!r} is missing."
        actual_mode = _mode(dpath)
        assert actual_mode == expected_mode, (
            f"Directory {dpath!r} has mode {oct(actual_mode)}, "
            f"expected {oct(expected_mode)}."
        )


def test_expected_files_exist_with_correct_size_content_and_permissions():
    """
    Verify presence, size, permissions, content and hash of the three
    reference files underneath /home/user/data/.
    """
    for fpath, (expected_size, expected_content) in EXPECTED_FILES.items():
        assert os.path.isfile(fpath), f"Required file {fpath!r} is missing."

        # Permissions
        actual_mode = _mode(fpath)
        expected_mode = 0o600
        assert actual_mode == expected_mode, (
            f"File {fpath!r} has mode {oct(actual_mode)}, "
            f"expected {oct(expected_mode)}."
        )

        # Size
        actual_size = os.path.getsize(fpath)
        assert actual_size == expected_size, (
            f"File {fpath!r} has size {actual_size} bytes, "
            f"expected {expected_size}."
        )

        # Content and checksum
        with open(fpath, "rb") as fh:
            data = fh.read()
        assert data == expected_content, (
            f"File {fpath!r} contains unexpected data."
        )
        # Optional: provide hash in failure message for easier debugging
        actual_hash = _sha256(data)
        expected_hash = _sha256(expected_content)
        assert actual_hash == expected_hash, (
            f"File {fpath!r} has SHA-256 {actual_hash}, "
            f"expected {expected_hash}."
        )


def test_no_extra_files_present():
    """
    Ensure that the data set contains *exactly* the three expected
    regular files and nothing else.
    """
    discovered_files = []
    for dirpath, _, filenames in os.walk(DATA_ROOT):
        for fname in filenames:
            discovered_files.append(os.path.join(dirpath, fname))

    expected_set = set(EXPECTED_FILES.keys())
    discovered_set = set(discovered_files)

    missing = expected_set - discovered_set
    unexpected = discovered_set - expected_set

    assert not missing, f"The following expected files are missing: {sorted(missing)}"
    assert not unexpected, (
        "Unexpected extra files found in /home/user/data: "
        f"{sorted(unexpected)}"
    )


def test_backup_archives_not_present_yet():
    """
    Before the student starts, no /home/user/backup_archives directory
    (nor any of its expected output files) should exist.
    """
    assert not os.path.exists(BACKUP_DIR), (
        f"Directory {BACKUP_DIR!r} already exists, but it should be created "
        "by the student during the exercise."
    )

    # Explicitly check the two filenames in case only the files exist
    # (symlinks, partial leftovers, etc.).
    for fname in ("weekly_data_backup.tar.gz", "backup_manifest.log"):
        path = os.path.join(BACKUP_DIR, fname)
        assert not os.path.exists(path), (
            f"Unexpected file {path!r} exists before the exercise starts."
        )