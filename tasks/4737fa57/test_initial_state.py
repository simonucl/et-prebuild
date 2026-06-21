# test_initial_state.py
#
# Pytest suite to validate the INITIAL state of the operating system
# before the student performs any action.
#
# This file checks that:
#   • /home/user/diagnostics exists and is a directory
#   • /home/user/diagnostics/collect-logs.log exists and is a regular file
#   • The log file is exactly three bytes long and contains the literal
#     ASCII characters “abc” with NO trailing newline.
#
# It deliberately does NOT look for the *.sha256 file, because that is an
# output artefact that should be created by the student.

import hashlib
from pathlib import Path

import pytest


DIAG_DIR = Path("/home/user/diagnostics")
LOG_FILE = DIAG_DIR / "collect-logs.log"
EXPECTED_LOG_CONTENT = b"abc"
EXPECTED_SHA256_HEX = hashlib.sha256(EXPECTED_LOG_CONTENT).hexdigest()


def test_diagnostics_directory_exists():
    """
    The /home/user/diagnostics directory must exist and be a directory.
    """
    assert DIAG_DIR.exists(), (
        "Required directory '/home/user/diagnostics' does not exist. "
        "Create it before proceeding with the exercise."
    )
    assert DIAG_DIR.is_dir(), (
        f"'{DIAG_DIR}' exists but is not a directory. "
        "Ensure it is a directory as expected."
    )


def test_log_file_exists():
    """
    The collect-logs.log file must exist inside the diagnostics directory.
    """
    assert LOG_FILE.exists(), (
        "Required file '/home/user/diagnostics/collect-logs.log' is missing. "
        "Place the log bundle at the specified location before continuing."
    )
    assert LOG_FILE.is_file(), (
        f"'{LOG_FILE}' exists but is not a regular file. "
        "Ensure it is a normal file, not a directory or special file."
    )


def test_log_file_content():
    """
    The log file must contain exactly the bytes 'abc' with no trailing newline.
    """
    content = LOG_FILE.read_bytes()
    assert content == EXPECTED_LOG_CONTENT, (
        "The contents of '/home/user/diagnostics/collect-logs.log' do not "
        "match the expected three bytes 'abc' (0x61 0x62 0x63). "
        f"Found: {content!r}"
    )
    assert len(content) == 3, (
        "The log file should be exactly 3 bytes long. "
        f"Actual length: {len(content)} bytes."
    )
    # Bonus sanity-check: confirm the SHA-256 hash matches the known value.
    digest = hashlib.sha256(content).hexdigest()
    assert digest == EXPECTED_SHA256_HEX, (
        "Unexpected SHA-256 digest for the log file. "
        f"Expected: {EXPECTED_SHA256_HEX}, got: {digest}."
    )