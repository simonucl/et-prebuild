# test_initial_state.py
#
# This pytest suite verifies that the operating-system / filesystem
# is in the correct **initial** state _before_ the student carries out
# the assignment described in the prompt.
#
# What we check:
# 1. All prerequisite files and directories exist and have the expected
#    properties and contents.
# 2. The reference checksum matches the actual checksum of app.conf.
# 3. The target output file (/home/user/checksums/verification.log)
#    does **not** yet exist.
#
# The tests purposefully fail with clear, instructive error messages
# if any pre-condition is violated.
#
# NOTE:  Only standard library and pytest are used.

import hashlib
from pathlib import Path

import pytest

# Absolute paths used throughout the assignment
APP_CONF            = Path("/home/user/project/app.conf")
CHECKSUMS_DIR       = Path("/home/user/checksums")
EXPECTED_SHA256     = CHECKSUMS_DIR / "expected.sha256"
VERIFICATION_LOG    = CHECKSUMS_DIR / "verification.log"

# ---------------------------------------------------------------------------


def test_project_structure():
    """Mandatory directories and files must already exist."""
    assert APP_CONF.exists(), f"Required file missing: {APP_CONF}"
    assert APP_CONF.is_file(), f"{APP_CONF} exists but is not a regular file"

    assert CHECKSUMS_DIR.exists(), f"Required directory missing: {CHECKSUMS_DIR}"
    assert CHECKSUMS_DIR.is_dir(), f"{CHECKSUMS_DIR} exists but is not a directory"

    assert EXPECTED_SHA256.exists(), f"Required file missing: {EXPECTED_SHA256}"
    assert EXPECTED_SHA256.is_file(), f"{EXPECTED_SHA256} exists but is not a regular file"


def test_app_conf_content():
    """app.conf must contain exactly the word 'hello' (no newline)."""
    content = APP_CONF.read_bytes()
    assert content == b"hello", (
        f"{APP_CONF} must contain exactly five bytes 'hello' "
        f"(no newline). Found: {content!r}"
    )


def test_expected_sha256_format_and_value():
    """
    expected.sha256 must:
    1. Contain exactly one line.
    2. Follow the conventional 'sha256  filename' format
       with two spaces between digest and filename.
    3. Hold a digest that matches the actual digest of app.conf.
    """
    lines = EXPECTED_SHA256.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1, f"{EXPECTED_SHA256} must contain exactly one line"
    line = lines[0]

    parts = line.split("  ")  # two spaces
    assert len(parts) == 2, (
        f"Line in {EXPECTED_SHA256!s} must have exactly two spaces between "
        "digest and filename"
    )

    digest_str, filename = parts
    assert filename == "app.conf", (
        f"{EXPECTED_SHA256} should reference 'app.conf' but found '{filename}'"
    )

    # Validate that the digest is a 64-char lowercase hex string
    assert (
        len(digest_str) == 64 and all(c in "0123456789abcdef" for c in digest_str)
    ), f"Digest in {EXPECTED_SHA256} is not a valid 64-character SHA-256 hex string"

    # Re-compute the actual digest of app.conf
    actual_digest = hashlib.sha256(APP_CONF.read_bytes()).hexdigest()
    assert (
        digest_str == actual_digest
    ), f"Digest mismatch: expected {digest_str}, but app.conf hashes to {actual_digest}"


def test_verification_log_absent():
    """
    The output file 'verification.log' must NOT exist yet. Creation of this
    file is part of the student's task; its pre-existence would indicate that
    the environment is not in the expected initial state.
    """
    assert not VERIFICATION_LOG.exists(), (
        f"{VERIFICATION_LOG} already exists, but it should be created only by "
        "the student's solution script. Remove it to start with a clean state."
    )