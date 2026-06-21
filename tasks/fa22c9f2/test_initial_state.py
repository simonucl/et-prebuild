# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem
# state for the “checksum verification” exercise.  These tests must all
# pass *before* the student performs any action.
#
# The suite checks:
#   • Required directories exist under /home/user/project
#   • assets/blank.js exists, is a zero-byte file and has the expected SHA-256
#   • checksums/sha256sums.txt exists and contains the exact expected line
#   • No premature verification.log file is present
#
# Only Python’s stdlib and pytest are used.

import hashlib
from pathlib import Path

import pytest

PROJECT_ROOT = Path("/home/user/project")
ASSETS_DIR = PROJECT_ROOT / "assets"
CHECKSUMS_DIR = PROJECT_ROOT / "checksums"
BLANK_JS = ASSETS_DIR / "blank.js"
SHA256SUMS_TXT = CHECKSUMS_DIR / "sha256sums.txt"
VERIFICATION_LOG = CHECKSUMS_DIR / "verification.log"

EXPECTED_SHA256 = (
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
)
EXPECTED_SHA256_LINE = (
    f"{EXPECTED_SHA256}  assets/blank.js\n"  # two spaces between hash and path
)


def test_project_root_exists():
    assert PROJECT_ROOT.is_dir(), (
        f"Required directory {PROJECT_ROOT} is missing. "
        "The project skeleton must be located at /home/user/project."
    )


def test_required_directories_exist():
    missing = [p for p in (ASSETS_DIR, CHECKSUMS_DIR) if not p.is_dir()]
    assert not missing, (
        "Missing required directories: "
        + ", ".join(str(p) for p in missing)
        + ". Ensure the project skeleton is intact."
    )


def test_blank_js_exists_and_zero_bytes():
    assert BLANK_JS.is_file(), f"File {BLANK_JS} is missing."
    size = BLANK_JS.stat().st_size
    assert size == 0, (
        f"Expected {BLANK_JS} to be zero bytes, but it is {size} byte(s)."
    )


def test_blank_js_checksum():
    digest = hashlib.sha256(BLANK_JS.read_bytes()).hexdigest()
    assert digest == EXPECTED_SHA256, (
        f"SHA-256 of {BLANK_JS} differs from expectation.\n"
        f"  Expected: {EXPECTED_SHA256}\n"
        f"  Found   : {digest}"
    )


def test_sha256sums_file_exists_and_contents():
    assert SHA256SUMS_TXT.is_file(), f"File {SHA256SUMS_TXT} is missing."

    contents = SHA256SUMS_TXT.read_text(encoding="utf-8")
    assert contents == EXPECTED_SHA256_LINE, (
        f"Incorrect content in {SHA256SUMS_TXT}.\n"
        "Expected exactly (including spaces and final newline):\n"
        f"{EXPECTED_SHA256_LINE!r}\n"
        "Found:\n"
        f"{contents!r}"
    )


def test_verification_log_not_present_yet():
    assert not VERIFICATION_LOG.exists(), (
        f"{VERIFICATION_LOG} should NOT exist before the student runs the "
        "verification step."
    )