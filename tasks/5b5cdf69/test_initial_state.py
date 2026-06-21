# test_initial_state.py
#
# This pytest suite validates the *initial* operating-system / filesystem state
# before the student starts working.  It checks that the supplied archive and its
# reference .sha256 file are present and correct, and that the workspace
# directory `/home/user/verify_logs` has **not** been created yet.
#
# NOTE:  • Only the Python standard library + pytest are used.
#        • Paths are always absolute.
#        • Failure messages are explicit so the learner knows what is missing.

import os
from pathlib import Path
import hashlib
import pytest
import subprocess

# CONSTANTS --------------------------------------------------------------------

ARCHIVES_DIR = Path("/home/user/archives")
BACKUP_FILE = ARCHIVES_DIR / "backup_20231015.tar.gz"
SHA256_FILE = ARCHIVES_DIR / "backup_20231015.tar.gz.sha256"
VERIFY_LOGS_DIR = Path("/home/user/verify_logs")

# EXPECTED VALUES --------------------------------------------------------------

# Expected SHA-256 digest for an empty file (tar.gz is 0-byte by spec here)
EMPTY_SHA256 = (
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
)
SHA256_LINE_EXPECTED = (
    f"{EMPTY_SHA256}  backup_20231015.tar.gz\n"  # two spaces, newline at end
)


# TESTS ------------------------------------------------------------------------

def test_archives_directory_exists():
    """/home/user/archives must exist and be a directory."""
    assert ARCHIVES_DIR.is_dir(), (
        f"Required directory missing: {ARCHIVES_DIR}"
    )


def test_backup_file_exists_and_is_empty():
    """
    /home/user/archives/backup_20231015.tar.gz must exist, be a regular file,
    and be exactly 0 bytes in size.
    """
    assert BACKUP_FILE.is_file(), (
        f"Required archive file missing: {BACKUP_FILE}"
    )
    size = BACKUP_FILE.stat().st_size
    assert size == 0, (
        f"{BACKUP_FILE} should be 0 bytes but is {size} bytes"
    )


def test_sha256_companion_file_contents():
    """
    The companion .sha256 file must exist, contain exactly one line, and that
    line must match the canonical sha256sum output (hash + two spaces +
    filename + newline).
    """
    assert SHA256_FILE.is_file(), (
        f"Required SHA-256 file missing: {SHA256_FILE}"
    )

    contents = SHA256_FILE.read_text(encoding="utf-8", errors="strict")
    lines = contents.splitlines(keepends=True)
    assert len(lines) == 1, (
        f"{SHA256_FILE} must contain exactly one line; found {len(lines)} lines"
    )
    assert lines[0] == SHA256_LINE_EXPECTED, (
        f"{SHA256_FILE} content mismatch.\n"
        f"Expected: {repr(SHA256_LINE_EXPECTED)}\n"
        f"Found:    {repr(lines[0])}"
    )

    # Extra check that the hash corresponds to the empty archive.
    archive_digest = hashlib.sha256(BACKUP_FILE.read_bytes()).hexdigest()
    assert archive_digest == EMPTY_SHA256, (
        "SHA-256 of the archive does not match the expected empty-file digest.\n"
        f"Expected: {EMPTY_SHA256}\n"
        f"Found:    {archive_digest}"
    )


def test_verify_logs_directory_absent():
    """
    /home/user/verify_logs must NOT exist yet—students are expected to create it.
    """
    assert not VERIFY_LOGS_DIR.exists(), (
        f"{VERIFY_LOGS_DIR} already exists, but it should be created by the "
        "student script, not beforehand."
    )


def test_dpkg_query_available_for_gzip():
    """
    dpkg-query should be available and able to report the installed gzip version
    (no sudo required).  This mirrors what the student will have to do later.
    """
    try:
        result = subprocess.run(
            ["dpkg-query", "-W", "-f=${Version}\n", "gzip"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except FileNotFoundError:
        pytest.fail(
            "The command 'dpkg-query' is not available but is required to "
            "check the gzip package version."
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(
            "Failed to query gzip version via dpkg-query. stderr:\n"
            f"{e.stderr}"
        )

    version_str = result.stdout.strip()
    assert version_str, "dpkg-query returned an empty version string for gzip."