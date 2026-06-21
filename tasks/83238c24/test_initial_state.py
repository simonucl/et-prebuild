# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system/filesystem state
# before the student performs any actions for the “db_ssl” task.
#
# Requirements verified:
# 1. /home/user/sample_certs exists and contains ca.pem
# 2. /home/user/sample_certs/ca.pem has the exact 5-byte payload “test”
#    and the expected SHA-256 digest.
# 3. /home/user/db_ssl (the target directory the student will create)
#    must not exist yet—its presence would indicate work was done
#    before the grader’s “initial-state” checks run.
#
# NOTE: Only Python’s standard library and pytest are used.

import hashlib
import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
SAMPLE_CERTS_DIR = HOME / "sample_certs"
SOURCE_CA = SAMPLE_CERTS_DIR / "ca.pem"
TARGET_DIR = HOME / "db_ssl"
EXPECTED_CA_CONTENT = b"test"
EXPECTED_SHA256 = (
    "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"
)


def sha256_hex(path: Path) -> str:
    """Return the hexadecimal SHA-256 digest of the given file."""
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(8192), b""):
            h.update(block)
    return h.hexdigest()


def test_sample_certs_directory_exists():
    assert SAMPLE_CERTS_DIR.exists(), (
        f"Required directory {SAMPLE_CERTS_DIR} is missing. "
        "The initial state must contain this directory."
    )
    assert SAMPLE_CERTS_DIR.is_dir(), (
        f"{SAMPLE_CERTS_DIR} exists but is not a directory."
    )


def test_source_ca_pem_exists_and_is_file():
    assert SOURCE_CA.exists(), (
        f"Required certificate file {SOURCE_CA} is missing."
    )
    assert SOURCE_CA.is_file(), f"{SOURCE_CA} exists but is not a regular file."


def test_source_ca_pem_contents_and_sha256():
    data = SOURCE_CA.read_bytes()
    assert data == EXPECTED_CA_CONTENT, (
        f"{SOURCE_CA} contents differ from expected 5-byte payload "
        f"'test'. Found {len(data)} bytes."
    )

    digest = sha256_hex(SOURCE_CA)
    assert (
        digest == EXPECTED_SHA256
    ), f"SHA-256 digest mismatch for {SOURCE_CA}. Expected {EXPECTED_SHA256}, got {digest}."


def test_target_directory_not_present_yet():
    assert not TARGET_DIR.exists(), (
        f"Directory {TARGET_DIR} already exists. "
        "The student task has not yet been performed, so this path should be absent."
    )