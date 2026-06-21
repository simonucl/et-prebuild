# test_initial_state.py
#
# Pytest suite that validates the *initial* filesystem state before the
# learner begins the exercise “convert UTF-16LE report to UTF-8”.
#
# The tests purposefully **fail** if:
#   • The source directory or file is missing.
#   • The source file is not UTF-16LE with a BOM.
#   • The decoded text is not exactly the three expected lines
#     (including the trailing newline on the last line).
#   • The target artefacts that the learner is supposed to create
#     already exist.
#
# Only Python’s stdlib and pytest are used.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
SCAN_DIR = HOME / "scan_outputs"
SRC_FILE = SCAN_DIR / "vuln_scan_utf16le.txt"
TARGET_FILE = SCAN_DIR / "vuln_scan_utf8.txt"
LOG_FILE = SCAN_DIR / "conversion.log"

EXPECTED_TEXT = (
    "Open port: 22/ssh\n"
    "Deprecated protocol: SSLv3 detected\n"
    "Vulnerability: CVE-2023-1234\n"
)

@pytest.mark.order(1)
def test_scan_directory_exists():
    assert SCAN_DIR.is_dir(), (
        f"Required directory {SCAN_DIR} is missing. "
        "The exercise expects this directory to be present before you start."
    )

@pytest.mark.order(2)
def test_source_file_exists_with_bom_and_is_utf16le():
    # 1. File existence
    assert SRC_FILE.is_file(), (
        f"Source file {SRC_FILE} is missing. It must exist prior to the task."
    )

    # 2. File has UTF-16LE BOM (0xFF 0xFE)
    with SRC_FILE.open("rb") as fh:
        first_two = fh.read(2)
    assert first_two == b"\xFF\xFE", (
        f"Source file {SRC_FILE} must start with a UTF-16LE BOM (0xFF 0xFE). "
        "Found different bytes."
    )

@pytest.mark.order(3)
def test_source_file_decodes_to_expected_content():
    # Use encoding='utf-16' so Python eats the BOM and chooses the endianness.
    decoded_text = SRC_FILE.read_text(encoding="utf-16")
    assert decoded_text == EXPECTED_TEXT, (
        "Decoded content of the source file is not what the exercise specifies.\n"
        f"Expected:\n{EXPECTED_TEXT!r}\n\nGot:\n{decoded_text!r}"
    )

    # Confirm there are exactly 3 lines when splitting on LF
    lines = decoded_text.splitlines()
    assert len(lines) == 3, (
        "Source file should contain exactly 3 lines after decoding, "
        f"but {len(lines)} were found."
    )

@pytest.mark.order(4)
def test_target_files_do_not_yet_exist():
    # Students must create these; they should not exist beforehand.
    for path in (TARGET_FILE, LOG_FILE):
        assert not path.exists(), (
            f"{path} already exists, but it should be created **by the student**, "
            "not be present in the initial state."
        )