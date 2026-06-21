# test_initial_state.py
#
# Pytest suite that validates the pristine state *before* the student runs any
# commands for the “backup-integrity” task.
#
# What we verify:
#   1. Required directories exist.
#   2. Required data files are present and are empty.
#   3. The reference checksum file exists and has the exact expected content.
#   4. The integrity-check log file does *not* exist yet.
#
# Only Python stdlib + pytest are used.

import hashlib
from pathlib import Path

import pytest

HOME = Path("/home/user")
DAILY_DIR = HOME / "backups" / "daily"
LOGS_DIR = HOME / "logs"

DATA_FILES = ["data1.txt", "data2.txt", "data3.txt"]
EXPECTED_SHA256_FILE = DAILY_DIR / "expected_sha256.txt"
EXPECTED_EMPTY_SHA256 = (
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
)
INTEGRITY_LOG = LOGS_DIR / "backup_integrity_check.log"


def sha256_of_bytes(data: bytes) -> str:
    """Return the hex-digest SHA-256 of *data*."""
    return hashlib.sha256(data).hexdigest()


@pytest.mark.parametrize("directory", [DAILY_DIR, LOGS_DIR])
def test_required_directories_exist(directory):
    assert directory.exists(), f"Required directory {directory} is missing."
    assert directory.is_dir(), f"{directory} exists but is not a directory."


@pytest.mark.parametrize("filename", DATA_FILES)
def test_data_files_exist_and_empty(filename):
    file_path = DAILY_DIR / filename
    assert file_path.exists(), f"Missing data file: {file_path}"
    assert file_path.is_file(), f"{file_path} exists but is not a regular file."

    # Check that the file is exactly 0 bytes
    size = file_path.stat().st_size
    assert size == 0, (
        f"{file_path} is expected to be empty (0 bytes) but is {size} bytes."
    )

    # Double-check the SHA-256 of the empty file
    with file_path.open("rb") as fh:
        data = fh.read()
    digest = sha256_of_bytes(data)
    assert (
        digest == EXPECTED_EMPTY_SHA256
    ), f"SHA-256 mismatch for {file_path}: expected {EXPECTED_EMPTY_SHA256}, got {digest}"


def test_expected_sha256_file_contents_exact_match():
    assert EXPECTED_SHA256_FILE.exists(), (
        f"Reference checksum file {EXPECTED_SHA256_FILE} is missing."
    )
    assert EXPECTED_SHA256_FILE.is_file(), (
        f"{EXPECTED_SHA256_FILE} exists but is not a regular file."
    )

    expected_lines = [
        f"{EXPECTED_EMPTY_SHA256}  data1.txt\n",
        f"{EXPECTED_EMPTY_SHA256}  data2.txt\n",
        f"{EXPECTED_EMPTY_SHA256}  data3.txt\n",
    ]

    with EXPECTED_SHA256_FILE.open("r", encoding="utf-8") as fh:
        content = fh.readlines()

    assert (
        content == expected_lines
    ), "Content of expected_sha256.txt does not match the required reference."


def test_integrity_log_does_not_exist_yet():
    assert (
        not INTEGRITY_LOG.exists()
    ), f"{INTEGRITY_LOG} should not exist before the verification command is run."