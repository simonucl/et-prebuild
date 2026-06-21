# test_initial_state.py
#
# Pytest suite that validates the operating-system / file-system **before**
# the student performs any action for the “backup-integrity engineer” task.
#
# Only the Python standard library and pytest are used.
# Failures intentionally include clear, actionable messages.

import hashlib
import os
import tarfile
from pathlib import Path

import pytest


# --------------------------------------------------------------------------- #
# Constants – hard-coded absolute paths that must exist before the task begins
# --------------------------------------------------------------------------- #
HOME = Path("/home/user")
BACKUPS_DIR = HOME / "backups"
ARCHIVE_PATH = BACKUPS_DIR / "weekly_backup.tar.gz"
EXPECTED_SHA_FILE = BACKUPS_DIR / "expected_sha256.txt"
AUDIT_DIR = HOME / "backup_audit"


# ----------------------------- Helper functions ---------------------------- #
def sha256_of_file(path: Path) -> str:
    """Return the hexadecimal SHA-256 digest of a file (binary mode, streamed)."""
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()


# --------------------------------- Tests ---------------------------------- #
def test_required_backup_files_exist():
    """Both the archive and the expected-hash file must already be present."""
    assert ARCHIVE_PATH.is_file(), (
        f"Required archive not found: {ARCHIVE_PATH}"
    )
    assert EXPECTED_SHA_FILE.is_file(), (
        f"Required hash file not found: {EXPECTED_SHA_FILE}"
    )


def test_expected_sha256_file_contents():
    """
    The expected-hash file must contain exactly one line with:
    <64-char-hash><two spaces>weekly_backup.tar.gz
    """
    content = EXPECTED_SHA_FILE.read_text(encoding="utf-8").rstrip("\n")
    parts = content.split("  ")  # two spaces
    assert len(parts) == 2, (
        f"{EXPECTED_SHA_FILE} should contain a hash, two spaces, and the "
        f"filename. Got: {content!r}"
    )
    expected_hash, filename = parts
    assert len(expected_hash) == 64 and all(c in "0123456789abcdef" for c in expected_hash), (
        f"First field in {EXPECTED_SHA_FILE} must be a 64-character hex digest."
    )
    assert filename == "weekly_backup.tar.gz", (
        f"Second field in {EXPECTED_SHA_FILE} must be 'weekly_backup.tar.gz', got {filename!r}"
    )


def test_actual_vs_expected_sha256_match():
    """The SHA-256 of the archive must match the value recorded in expected_sha256.txt."""
    expected_hash = EXPECTED_SHA_FILE.read_text(encoding="utf-8").split("  ")[0].strip()
    actual_hash = sha256_of_file(ARCHIVE_PATH)
    assert actual_hash == expected_hash, (
        "SHA-256 mismatch:\n"
        f"  Expected: {expected_hash}\n"
        f"    Actual: {actual_hash}\n"
        "The pre-loaded archive is corrupted or the expected hash is wrong."
    )


def test_archive_structure_and_contents():
    """
    The tar archive must contain exactly one file named 'hello.txt'
    whose contents are the single line 'Hello backup\\n'.
    """
    assert tarfile.is_tarfile(ARCHIVE_PATH), f"{ARCHIVE_PATH} is not a valid tar archive."
    with tarfile.open(ARCHIVE_PATH, "r:gz") as tf:
        names = tf.getnames()
        assert names == ["hello.txt"], (
            f"Archive should contain exactly one file 'hello.txt'. "
            f"Found: {names}"
        )
        member = tf.getmember("hello.txt")
        assert member.isfile(), "'hello.txt' inside archive is not a regular file."
        extracted_data = tf.extractfile(member).read()
        assert extracted_data == b"Hello backup\n", (
            f"'hello.txt' content mismatch. Expected b'Hello backup\\n', "
            f"got {extracted_data!r}"
        )
        # Also ensure there is no 'eval(' occurrence in the payload
        assert b"eval(" not in extracted_data, (
            "'hello.txt' unexpectedly contains the substring 'eval('"
        )


def test_audit_directory_not_present_yet():
    """
    The working directory /home/user/backup_audit/ must *not* exist
    before the student runs their solution.
    """
    assert not AUDIT_DIR.exists(), (
        f"{AUDIT_DIR} already exists, but it should be created by the student's "
        "script during execution, not beforehand."
    )