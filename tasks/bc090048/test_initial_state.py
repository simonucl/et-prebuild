# test_initial_state.py
#
# Pytest suite that validates the **initial** state of the filesystem as
# described in the assignment.  These checks run *before* the student’s
# solution is executed, ensuring the prerequisite files and their exact
# contents are in place.
#
# NOTE:  We intentionally do **not** test for the presence or content of the
#        output file `/home/user/checksum_verification.log`, because that file
#        should not exist yet.

import hashlib
import os
from pathlib import Path
import pytest

# ---------------------------------------------------------------------------
# Constants & helpers
# ---------------------------------------------------------------------------

BASE_DIR = Path("/home/user/config_backups")

CONF_FILES = {
    "fw01.conf": {
        "expected_content": b"abc",  # no trailing newline
        "sha256": "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
    },
    "sw02.conf": {
        "expected_content": b"hello world",  # no trailing newline
        "sha256": "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9",
    },
    "rtr03.conf": {
        "expected_content": b"",  # empty file
        "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    },
}

REFERENCE_CSV_PATH = BASE_DIR / "reference_checksums.csv"

REFERENCE_CSV_LINES = [
    "FILENAME,SHA256\n",
    "fw01.conf,ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad\n",
    "sw02.conf,b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9\n",
    "rtr03.conf,e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855\n",
]


def sha256_of_bytes(data: bytes) -> str:
    """Return the hex-encoded SHA-256 digest of *data*."""
    return hashlib.sha256(data).hexdigest()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_config_backups_directory_exists():
    """/home/user/config_backups must exist and be a directory."""
    assert BASE_DIR.exists(), f"Required directory {BASE_DIR} is missing."
    assert BASE_DIR.is_dir(), f"{BASE_DIR} exists but is not a directory."


@pytest.mark.parametrize("filename,meta", CONF_FILES.items())
def test_conf_file_presence_and_content(filename, meta):
    """
    Ensure each required .conf file exists, has the exact expected content,
    and matches the authoritative SHA-256 value.
    """
    full_path = BASE_DIR / filename

    # Presence check
    assert full_path.exists(), f"Required file {full_path} is missing."
    assert full_path.is_file(), f"{full_path} exists but is not a regular file."

    # Read raw bytes
    data = full_path.read_bytes()

    # Content check
    assert (
        data == meta["expected_content"]
    ), f"Content of {full_path} does not match the expected bytes."

    # SHA-256 check
    actual_sha = sha256_of_bytes(data)
    expected_sha = meta["sha256"]
    assert (
        actual_sha == expected_sha
    ), f"SHA-256 mismatch for {full_path}: expected {expected_sha}, got {actual_sha}."


def test_reference_csv_exists():
    """Verify that reference_checksums.csv exists and is a regular, readable file."""
    assert REFERENCE_CSV_PATH.exists(), (
        f"Required file {REFERENCE_CSV_PATH} is missing."
    )
    assert REFERENCE_CSV_PATH.is_file(), (
        f"{REFERENCE_CSV_PATH} exists but is not a regular file."
    )


def test_reference_csv_exact_content():
    """
    The reference CSV must contain exactly four newline-terminated lines as
    specified, with no extra whitespace or lines.
    """
    # Read file as binary so we can check for final newline byte unambiguously.
    raw = REFERENCE_CSV_PATH.read_bytes()

    # Must end with a single LF
    assert raw.endswith(b"\n"), (
        f"{REFERENCE_CSV_PATH} must be terminated by a single Unix newline."
    )

    # Split into text lines
    lines = raw.decode("utf-8").splitlines(keepends=True)

    # Must have exactly four lines (header + three data rows)
    assert len(lines) == 4, (
        f"{REFERENCE_CSV_PATH} must contain exactly 4 lines; found {len(lines)}."
    )

    # Content must match exactly what the spec says
    for idx, (expected, actual) in enumerate(zip(REFERENCE_CSV_LINES, lines), start=1):
        assert (
            actual == expected
        ), f"Line {idx} of {REFERENCE_CSV_PATH!s} is incorrect.\nExpected: {expected!r}\nActual:   {actual!r}"


def test_reference_csv_hashes_match_conf_files():
    """
    Cross-validate that the authoritative SHA-256 values listed in the CSV
    exactly match those of the current .conf files.
    """
    # Build mapping from CSV
    csv_mapping = {}
    with REFERENCE_CSV_PATH.open(encoding="utf-8") as fp:
        next(fp)  # skip header
        for line in fp:
            file_name, sha_value = line.strip().split(",", maxsplit=1)
            csv_mapping[file_name] = sha_value

    # Check each .conf file
    for file_name, sha_value in csv_mapping.items():
        path = BASE_DIR / file_name
        assert path.exists(), f"File listed in CSV but missing on disk: {path}"
        actual_sha = sha256_of_bytes(path.read_bytes())
        assert (
            actual_sha == sha_value
        ), f"SHA-256 mismatch: CSV lists {sha_value} for {file_name}, but on-disk file hashes to {actual_sha}."


# ---------------------------------------------------------------------------
# End of test_initial_state.py
# ---------------------------------------------------------------------------