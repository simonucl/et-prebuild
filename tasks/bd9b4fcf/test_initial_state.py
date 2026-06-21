# test_initial_state.py
#
# This pytest suite verifies that the operating-system state is exactly as
# expected *before* the student performs any action for the “archive checksum
# verification” exercise.
#
# What must already exist:
#   1. /home/user/backup/old_project.tar.gz       (4-byte file: b"test")
#   2. /home/user/backup/checksums.txt            (one precise SHA-256 line)
#
# What must *not* yet exist:
#   • /home/user/backup/integrity_report.log      (created by the student later)
#
# The tests below will fail with clear, actionable messages if any of the
# pre-conditions are violated.

import hashlib
import os
from pathlib import Path

BACKUP_DIR = Path("/home/user/backup")
ARCHIVE      = BACKUP_DIR / "old_project.tar.gz"
CHECKSUMS_TXT = BACKUP_DIR / "checksums.txt"
REPORT_LOG   = BACKUP_DIR / "integrity_report.log"

EXPECTED_HASH = "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"
EXPECTED_LINE = f"{EXPECTED_HASH}  old_project.tar.gz\n"  # note two spaces

def test_backup_directory_exists():
    assert BACKUP_DIR.is_dir(), (
        f"Required directory {BACKUP_DIR} is missing. "
        "Create it exactly at that absolute path."
    )

def test_archive_file_correct():
    assert ARCHIVE.is_file(), f"Archive file {ARCHIVE} is missing."
    size = ARCHIVE.stat().st_size
    assert size == 4, (
        f"Archive {ARCHIVE} must be 4 bytes long, found {size} bytes."
    )
    content = ARCHIVE.read_bytes()
    assert content == b"test", (
        f"Archive {ARCHIVE} should contain the ASCII word 'test' "
        f"(hex: 74 65 73 74). Found: {content!r}"
    )

    sha256 = hashlib.sha256(content).hexdigest()
    assert sha256 == EXPECTED_HASH, (
        f"SHA-256 hash of {ARCHIVE} is {sha256}, expected {EXPECTED_HASH}. "
        "The file contents are incorrect."
    )

def test_checksums_txt_correct():
    assert CHECKSUMS_TXT.is_file(), f"Checksum file {CHECKSUMS_TXT} is missing."
    text = CHECKSUMS_TXT.read_text(encoding="utf-8")
    assert text == EXPECTED_LINE, (
        f"{CHECKSUMS_TXT} must contain exactly one line:\n"
        f"    {EXPECTED_LINE!r}\n"
        f"Found instead:\n"
        f"    {text!r}"
    )

def test_integrity_report_not_present_yet():
    assert not REPORT_LOG.exists(), (
        f"{REPORT_LOG} already exists but should be created only after the "
        "student runs their solution. Remove this file before starting."
    )