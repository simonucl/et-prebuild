# test_initial_state.py
#
# Pytest suite that validates the *initial* filesystem state for the
# “backup-integrity” exercise.  These tests must all pass *before* the
# learner performs any of the required actions.  They confirm that the
# pre-populated directory layout, file names, contents and checksums are
# exactly as expected, and that no output files created by the upcoming
# task are present yet.
#
# Only Python’s standard library and pytest are used.

import hashlib
import os
from pathlib import Path

import pytest

# Constants ------------------------------------------------------------------

BACKUP_ROOT = Path("/home/user/backup")
BACKUP_DATE = "2023-09-15"
BACKUP_DIR = BACKUP_ROOT / BACKUP_DATE

REQUIRED_FILES = {
    "original1.txt": "a",
    "original2.txt": "abc",
    "original3.txt": "",  # empty file
}

CHECKSUM_FILE = BACKUP_DIR / "checksums.sha256"
INTEGRITY_LOG = BACKUP_ROOT / "integrity.log"
INTEGRITY_SUMMARY = BACKUP_ROOT / "integrity_summary.txt"

EXPECTED_CHECKSUM_LINES = (
    "ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb  original1.txt\n"
    "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad  original2.txt\n"
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  original3.txt\n"
)


# Helper ---------------------------------------------------------------------

def sha256_of(path: Path) -> str:
    """Return the hex-encoded SHA-256 digest of a file."""
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()


# Tests ----------------------------------------------------------------------

def test_backup_directory_exists():
    assert BACKUP_DIR.exists(), (
        f"Required directory {BACKUP_DIR} is missing."
    )
    assert BACKUP_DIR.is_dir(), (
        f"{BACKUP_DIR} exists but is not a directory."
    )


def test_required_files_present_and_no_extraneous_files():
    present_files = {p.name for p in BACKUP_DIR.iterdir() if p.is_file()}
    expected_files = set(REQUIRED_FILES) | {"checksums.sha256"}
    missing = expected_files - present_files
    extra = present_files - expected_files
    assert not missing, (
        f"Missing required file(s) in {BACKUP_DIR}: {', '.join(sorted(missing))}"
    )
    assert not extra, (
        f"Unexpected extra file(s) present in {BACKUP_DIR}: {', '.join(sorted(extra))}"
    )


@pytest.mark.parametrize("filename,expected_contents", REQUIRED_FILES.items())
def test_individual_file_contents(filename, expected_contents):
    path = BACKUP_DIR / filename
    assert path.exists(), f"Expected file {path} not found."
    actual = path.read_text()
    assert actual == expected_contents, (
        f"File {path} has unexpected contents.\n"
        f"Expected: {repr(expected_contents)}\n"
        f"Found:    {repr(actual)}"
    )


def test_checksums_file_content_exact():
    assert CHECKSUM_FILE.exists(), f"{CHECKSUM_FILE} not found."
    actual = CHECKSUM_FILE.read_text()
    assert actual == EXPECTED_CHECKSUM_LINES, (
        f"{CHECKSUM_FILE} contents are incorrect or have unexpected "
        f"whitespace/blank lines."
    )


def test_checksums_match_actual_files():
    # Parse the checksums.sha256 file and verify each digest matches
    with CHECKSUM_FILE.open() as fh:
        for line in fh:
            digest, filename = line.rstrip("\n").split(maxsplit=1)
            # The specification uses two spaces between digest and filename;
            # using split(maxsplit=1) handles that correctly.
            path = BACKUP_DIR / filename.strip()
            assert path.exists(), f"File listed in checksums but missing: {path}"
            actual_digest = sha256_of(path)
            assert actual_digest == digest, (
                f"SHA-256 mismatch for {path}.\n"
                f"Expected: {digest}\n"
                f"Found:    {actual_digest}"
            )


def test_output_files_do_not_exist_yet():
    for path in (INTEGRITY_LOG, INTEGRITY_SUMMARY):
        assert not path.exists(), (
            f"{path} should NOT exist yet – it must be created by the learner’s solution."
        )