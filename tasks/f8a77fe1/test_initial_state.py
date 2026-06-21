# test_initial_state.py
"""
Pytest suite that validates the operating-system state *before* the student
runs any command for the “SHA-256 compliance audit” exercise.

Truth we assert:
1. /home/user/compliance_docs/passwd_policy_v1.2.txt
   • exists,
   • is a regular file,
   • is exactly 0 bytes long,
   • is world-readable (other-read bit set).
2. /home/user/audit_log directory does NOT exist (yet).
3. The SHA-256 digest of the empty file matches the known value
   e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855.
"""

import hashlib
import os
import stat
import pytest

COMPLIANCE_FILE = "/home/user/compliance_docs/passwd_policy_v1.2.txt"
AUDIT_LOG_DIR = "/home/user/audit_log"
EMPTY_SHA256 = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"


def test_compliance_file_exists_and_is_regular():
    assert os.path.exists(COMPLIANCE_FILE), (
        f"Expected file {COMPLIANCE_FILE!r} to exist."
    )
    assert os.path.isfile(COMPLIANCE_FILE), (
        f"Expected {COMPLIANCE_FILE!r} to be a regular file, "
        "but it is not."
    )


def test_compliance_file_is_empty():
    size = os.path.getsize(COMPLIANCE_FILE)
    assert size == 0, (
        f"Expected {COMPLIANCE_FILE!r} to be 0 bytes, but it is {size} bytes."
    )


def test_compliance_file_is_world_readable():
    mode = os.stat(COMPLIANCE_FILE).st_mode
    is_world_readable = bool(mode & stat.S_IROTH)
    assert is_world_readable, (
        f"Expected {COMPLIANCE_FILE!r} to be world-readable "
        "(other-read bit set), but permissions are {oct(mode & 0o777)}."
    )


def test_audit_log_directory_absent():
    assert not os.path.exists(AUDIT_LOG_DIR), (
        f"Directory {AUDIT_LOG_DIR!r} should NOT exist before the student "
        "runs their command."
    )


def test_empty_file_sha256_digest():
    with open(COMPLIANCE_FILE, "rb") as fp:
        digest = hashlib.sha256(fp.read()).hexdigest()
    assert digest == EMPTY_SHA256, (
        "SHA-256 digest of the empty compliance document is incorrect.\n"
        f"Expected: {EMPTY_SHA256}\n"
        f"Got     : {digest}"
    )