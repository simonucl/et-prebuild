# test_initial_state.py
#
# This pytest suite validates the filesystem state **before** the student
# performs any actions for the “mock-API artefacts” task.
#
# What we verify:
# 1. /home/user/api_response.txt  → exists, exactly five bytes, contains “hello”
# 2. /home/user/reference.sha256 → exists, classic ‘sha256sum’ format,
#    stores the correct SHA-256 hash for the file above
# 3. /home/user/api_test/ and its sub-dirs do *not* exist yet
#
# NOTE: Do *not* add tests for any files the student is supposed to create
# (e.g. integrity.log).  We only assert the initial state.

import hashlib
from pathlib import Path
import re
import pytest


API_RESPONSE = Path("/home/user/api_response.txt")
REFERENCE_SHA = Path("/home/user/reference.sha256")
API_TEST_DIR = Path("/home/user/api_test")
HASH_HELLO = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"


def read_bytes(path: Path) -> bytes:
    try:
        return path.read_bytes()
    except FileNotFoundError:
        pytest.fail(f"Required file is missing: {path}")


def test_api_response_file_exists_and_content():
    """api_response.txt must exist, be 5 bytes long, contain ASCII ‘hello’, no trailing newline."""
    assert API_RESPONSE.exists(), f"File not found: {API_RESPONSE}"
    assert API_RESPONSE.is_file(), f"Not a regular file: {API_RESPONSE}"

    content = read_bytes(API_RESPONSE)
    assert len(content) == 5, (
        f"{API_RESPONSE} must be exactly 5 bytes long; found {len(content)} bytes"
    )
    assert content == b"hello", (
        f"{API_RESPONSE} must contain the bytes b'hello' (no newline); "
        f"found {content!r}"
    )


def test_reference_sha256_file_exists_and_format():
    """
    reference.sha256 must exist, contain one line in classic `sha256sum` format:
       <64-hex-digits><two spaces>api_response.txt\n
    and the hash must match the SHA-256 of 'hello'.
    """
    assert REFERENCE_SHA.exists(), f"File not found: {REFERENCE_SHA}"
    assert REFERENCE_SHA.is_file(), f"Not a regular file: {REFERENCE_SHA}"

    text = REFERENCE_SHA.read_text(encoding="utf-8")
    # Must end with a single newline
    assert text.endswith("\n"), (
        f"{REFERENCE_SHA} must end with exactly one newline character"
    )

    # Split lines and ensure single line
    lines = text.splitlines()
    assert len(lines) == 1, f"{REFERENCE_SHA} must contain exactly one line"
    line = lines[0]

    sha_line_re = re.compile(r"^[0-9a-f]{64}  api_response\.txt$")
    assert sha_line_re.match(line), (
        f"{REFERENCE_SHA} line must match '<64hex><two spaces>api_response.txt'; "
        f"got: {line!r}"
    )

    expected_hash = line.split("  ")[0]
    assert (
        expected_hash == HASH_HELLO
    ), f"Hash in {REFERENCE_SHA} is incorrect; expected {HASH_HELLO}, got {expected_hash}"

    # Compute actual SHA-256 of the api_response.txt file and compare
    actual_hash = hashlib.sha256(read_bytes(API_RESPONSE)).hexdigest()
    assert (
        actual_hash == expected_hash
    ), f"The SHA-256 of {API_RESPONSE} does not match the reference.\nExpected: {expected_hash}\nActual:   {actual_hash}"


def test_api_test_directory_absent():
    """/home/user/api_test/ (and its children) must not exist before the student runs their commands."""
    assert not API_TEST_DIR.exists(), (
        f"Directory {API_TEST_DIR} should NOT exist before the task is performed, "
        "but it is already present."
    )