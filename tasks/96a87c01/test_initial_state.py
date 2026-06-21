# test_initial_state.py
#
# This test-suite validates that the operating system / filesystem starts in the
# correct state *before* the student carries out the task described in the
# assignment.  It checks only the resources that must already exist and **does
# not** touch any of the files that the student will be expected to create
# (e.g. verification.log).

import hashlib
import os
from pathlib import Path

import pytest

# Constants for the paths and expected values in the initial state
DB_EXPORT_DIR = Path("/home/user/db_exports")
SQL_FILE = DB_EXPORT_DIR / "optimized_queries.sql"
EXPECTED_SHA256_EMPTY_FILE = (
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
)


def sha256_of_file(path: Path) -> str:
    """
    Compute the SHA-256 hexadecimal digest of the file at *path* using a single
    streaming pass (works even for very large files).
    """
    hash_obj = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(8192), b""):
            hash_obj.update(block)
    return hash_obj.hexdigest()


def test_db_export_directory_exists():
    assert DB_EXPORT_DIR.exists(), (
        f"Required directory {DB_EXPORT_DIR} is missing. "
        "Create it before proceeding."
    )
    assert DB_EXPORT_DIR.is_dir(), (
        f"{DB_EXPORT_DIR} exists but is not a directory."
    )


def test_sql_file_exists_and_is_empty():
    assert SQL_FILE.exists(), (
        f"Required file {SQL_FILE} is missing. "
        "The assignment expects it to be present before you begin."
    )
    assert SQL_FILE.is_file(), (
        f"{SQL_FILE} exists but is not a regular file."
    )

    size = SQL_FILE.stat().st_size
    assert size == 0, (
        f"{SQL_FILE} should be an empty file (0 bytes) in the initial state, "
        f"but its size is {size} bytes."
    )


def test_sql_file_sha256_matches_empty_file_digest():
    calculated_digest = sha256_of_file(SQL_FILE)
    assert (
        calculated_digest == EXPECTED_SHA256_EMPTY_FILE
    ), (
        "SHA-256 digest of the initial SQL file does not match that of an empty "
        "file. The file may have been modified unexpectedly.\n"
        f"Expected: {EXPECTED_SHA256_EMPTY_FILE}\n"
        f"Actual:   {calculated_digest}"
    )