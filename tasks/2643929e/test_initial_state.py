# test_initial_state.py
#
# Pytest suite that validates the *initial* filesystem state before the
# student carries out the conversion task described in the assignment.
#
# The tests assert that:
#   • The source directory and the UTF-8 file exist and contain the exact
#     expected bytes / text.
#   • None of the artefacts that the student is asked to create are present
#     yet (Latin-1 copy, checksum file, log file).
#
# Only the Python standard library and pytest are used.

import os
import sys
import codecs
import pytest
from pathlib import Path

# --------------------------------------------------------------------------- #
# Paths (absolute, as required by the specification)

ROOT_DIR = Path("/home/user/project/pipelines/mobile")
UTF8_FILE = ROOT_DIR / "build-notes-utf8.txt"
LATIN1_FILE = ROOT_DIR / "build-notes-latin1.txt"
SHA256_FILE = ROOT_DIR / "build-notes-latin1.txt.sha256"
SUMMARY_LOG = ROOT_DIR / "conversion-summary.log"

# --------------------------------------------------------------------------- #
# Expected source-file bytes.
#
# Using the explicit hexadecimal sequence guarantees that the comparison is
# byte-for-byte and not influenced by the runtime’s default encoding.

_EXPECTED_UTF8_HEX = (
    "52 65 6c 65 61 73 65 3a 20 31 2e 32 2e 33 0a"
    "43 68 61 6e 67 65 6c 6f 67 3a 20 46 69 78 65 64 20"
    "72 c3 a9 73 75 6d c3 a9 20 70 61 72 73 69 6e 67 2c 20"
    "69 6d 70 72 6f 76 65 64 20 55 49 20 66 6f 72 20"
    "5a c3 bc 72 69 63 68 0a"
    "41 75 74 68 6f 72 3a 20 4a 6f 73 c3 a9 20"
    "c3 81 6c 76 61 72 65 7a 0a"
)
EXPECTED_UTF8_BYTES = bytes.fromhex(_EXPECTED_UTF8_HEX)
EXPECTED_UTF8_SIZE = 97  # bytes

# Convenience: the decoded UTF-8 text (for readability assertions)
EXPECTED_TEXT = (
    "Release: 1.2.3\n"
    "Changelog: Fixed résumé parsing, improved UI for Zürich\n"
    "Author: José Álvarez\n"
)

# --------------------------------------------------------------------------- #
# Helper

def _read_bytes(path: Path) -> bytes:
    with path.open("rb") as fh:
        return fh.read()

# --------------------------------------------------------------------------- #
# Tests

def test_directory_exists():
    """The pipeline directory must exist and be a directory."""
    assert ROOT_DIR.is_dir(), f"Required directory {ROOT_DIR} is missing."

def test_utf8_file_exists_and_is_correct():
    """Validate presence, size and exact byte content of the UTF-8 source file."""
    assert UTF8_FILE.is_file(), f"File {UTF8_FILE} does not exist."
    actual_size = UTF8_FILE.stat().st_size
    assert actual_size == EXPECTED_UTF8_SIZE, (
        f"{UTF8_FILE} has size {actual_size}, expected {EXPECTED_UTF8_SIZE} bytes."
    )

    actual_bytes = _read_bytes(UTF8_FILE)
    assert actual_bytes == EXPECTED_UTF8_BYTES, (
        f"Byte content of {UTF8_FILE} does not match the expected initial state."
    )

    # Extra sanity check: the file decodes as UTF-8 to the expected string.
    try:
        decoded = actual_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        pytest.fail(f"{UTF8_FILE} is not valid UTF-8: {exc}")

    assert decoded == EXPECTED_TEXT, (
        f"Decoded text of {UTF8_FILE} does not match expected contents."
    )

def test_target_files_absent():
    """None of the artefacts that the student is supposed to create should exist yet."""
    for path in (LATIN1_FILE, SHA256_FILE, SUMMARY_LOG):
        assert not path.exists(), (
            f"{path} already exists, but the student has not performed the task yet."
        )