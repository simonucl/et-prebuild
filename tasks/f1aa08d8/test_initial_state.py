# test_initial_state.py
#
# This pytest suite validates the **initial** filesystem state before the
# student performs any actions.  It checks ONLY the pre-existing resources
# (input snapshot) and purposefully ignores all paths that will be created
# by the student (/home/user/backup_restore, /home/user/backup_logs, etc.)
# in accordance with the grading rules.

import hashlib
import os
from pathlib import Path

import pytest

SNAPSHOT_ROOT = Path("/home/user/backup_source").resolve()

# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def sha256sum(path: Path) -> str:
    """Return the SHA-256 hex digest (lower-case) of the given file."""
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# --------------------------------------------------------------------------- #
# Expected snapshot description
# --------------------------------------------------------------------------- #
EXPECTED_FILES = {
    SNAPSHOT_ROOT / "docs" / "report.txt": {
        "content": b"hello world",
        "sha256": "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9",
    },
    SNAPSHOT_ROOT / "images" / "logo.txt": {
        "content": b"abc",
        "sha256": "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
    },
}


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_snapshot_directory_exists_and_is_directory():
    assert SNAPSHOT_ROOT.exists(), (
        f"Required snapshot directory '{SNAPSHOT_ROOT}' is missing."
    )
    assert SNAPSHOT_ROOT.is_dir(), (
        f"'{SNAPSHOT_ROOT}' exists but is not a directory."
    )


@pytest.mark.parametrize("file_path", sorted(EXPECTED_FILES))
def test_expected_file_exists(file_path: Path):
    assert file_path.exists(), f"Expected file '{file_path}' is missing."
    assert file_path.is_file(), f"Expected file '{file_path}' is not a regular file."


@pytest.mark.parametrize("file_path,meta", EXPECTED_FILES.items())
def test_file_contents_and_checksum(file_path: Path, meta: dict):
    # Check file contents.
    actual_content = file_path.read_bytes()
    expected_content = meta["content"]
    assert (
        actual_content == expected_content
    ), f"File '{file_path}' content mismatch."

    # Check SHA-256 checksum.
    actual_sha = sha256sum(file_path)
    expected_sha = meta["sha256"]
    assert (
        actual_sha == expected_sha
    ), (
        f"File '{file_path}' SHA-256 mismatch:\n"
        f"  expected: {expected_sha}\n"
        f"  found:    {actual_sha}"
    )


def test_no_unexpected_files_present():
    """
    Ensure no extra files are lurking inside /home/user/backup_source.
    This guards against accidental pollution of the snapshot directory
    which could invalidate the restore verification later.
    """
    all_disk_files = {
        p for p in SNAPSHOT_ROOT.rglob("*") if p.is_file()
    }
    expected_files_set = set(EXPECTED_FILES.keys())

    unexpected = all_disk_files - expected_files_set
    missing = expected_files_set - all_disk_files

    assert not missing, (
        "The following expected file(s) are missing:\n  "
        + "\n  ".join(map(str, sorted(missing)))
    )
    assert not unexpected, (
        "Unexpected file(s) found in snapshot directory:\n  "
        + "\n  ".join(map(str, sorted(unexpected)))
    )