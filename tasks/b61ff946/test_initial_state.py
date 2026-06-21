# test_initial_state.py
#
# Pytest suite that validates the **initial** operating-system / filesystem
# state for the “backup-integrity” exercise *before* the student runs any
# verification commands.
#
# It checks that:
#   • The source and backup directories exist in the expected locations.
#   • Each directory contains exactly the two regular files: data1.txt, data2.txt
#     (and no others).
#   • The SHA-256 checksums of every file pair are byte-for-byte identical and
#     match the reference hashes hard-coded below.
#   • The report file /home/user/backup_verification.log is NOT present yet
#     (the student must create it).
#
# Only standard-library modules + pytest are used.

import hashlib
import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
SRC_DIR = HOME / "project_data"
BACKUP_DIR = HOME / "backup" / "project_data_copy"
REPORT_FILE = HOME / "backup_verification.log"

EXPECTED_FILES = ("data1.txt", "data2.txt")

# Reference SHA-256 values taken from the authoritative solution.
REFERENCE_HASHES = {
    "data1.txt": "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
    "data2.txt": "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08",
}


def sha256(path: Path) -> str:
    """Return hexadecimal SHA-256 digest of a file."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def test_directories_exist():
    assert SRC_DIR.is_dir(), f"Source directory missing: {SRC_DIR}"
    assert BACKUP_DIR.is_dir(), f"Backup directory missing: {BACKUP_DIR}"


@pytest.mark.parametrize("directory", [SRC_DIR, BACKUP_DIR])
def test_expected_files_present(directory: Path):
    for fname in EXPECTED_FILES:
        fpath = directory / fname
        assert fpath.is_file(), f"Expected file not found: {fpath}"


@pytest.mark.parametrize("directory", [SRC_DIR, BACKUP_DIR])
def test_no_extra_files(directory: Path):
    regular_files = sorted(
        f.name for f in directory.iterdir() if f.is_file()
    )
    assert regular_files == list(EXPECTED_FILES), (
        f"Directory {directory} contains unexpected files: {regular_files!r} "
        f"(expected exactly {EXPECTED_FILES})"
    )


def test_hashes_match_reference_and_each_other():
    for fname in EXPECTED_FILES:
        src_path = SRC_DIR / fname
        backup_path = BACKUP_DIR / fname

        src_hash = sha256(src_path)
        backup_hash = sha256(backup_path)
        ref_hash = REFERENCE_HASHES[fname]

        assert src_hash == ref_hash, (
            f"SHA-256 of {src_path} is {src_hash}, expected {ref_hash}"
        )
        assert backup_hash == ref_hash, (
            f"SHA-256 of {backup_path} is {backup_hash}, expected {ref_hash}"
        )
        assert src_hash == backup_hash, (
            f"Mismatch between source and backup for {fname}: "
            f"{src_hash} != {backup_hash}"
        )


def test_report_file_absent():
    assert not REPORT_FILE.exists(), (
        f"Report file {REPORT_FILE} already exists; the student should create it."
    )