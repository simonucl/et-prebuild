# test_initial_state.py
#
# Pytest suite that validates the operating-system / filesystem
# *before* the student starts working on the “one-touch” audit
# automation assignment.
#
# The checks assert the following ground-truth assumptions:
#
#   1. Directory layout
#      /home/user/compliance_audit/
#      └── sample_data/
#          ├── file1.txt   (empty file, 0 bytes)
#          └── file2.txt   (ASCII text “abc”, NO trailing newline)
#
#   2. Expected SHA-256 digests
#        sample_data/file1.txt  e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
#        sample_data/file2.txt  ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad
#
#   3. No Makefile or output artefacts should exist yet.
#
# If any of these assertions fail, the test output will explicitly
# identify what is missing or incorrect so the course staff can fix
# the base image before students begin.

import hashlib
import os
from pathlib import Path

# Constants -------------------------------------------------------------------

HOME = Path("/home/user")
AUDIT_DIR = HOME / "compliance_audit"
SAMPLE_DIR = AUDIT_DIR / "sample_data"

FILE1 = SAMPLE_DIR / "file1.txt"
FILE2 = SAMPLE_DIR / "file2.txt"

EXPECTED_SHA256 = {
    FILE1: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    FILE2: "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
}

OUTPUT_FILES = [
    AUDIT_DIR / "file_list.log",
    AUDIT_DIR / "checksum.log",
    AUDIT_DIR / "audit.log",
]

MAKEFILE_PATH = AUDIT_DIR / "Makefile"


# Helper ----------------------------------------------------------------------

def sha256_hex(path: Path) -> str:
    """Return the SHA-256 hex digest of *path*."""
    h = hashlib.sha256()
    with path.open("rb") as fp:
        for chunk in iter(lambda: fp.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# Tests -----------------------------------------------------------------------

def test_directories_present():
    assert AUDIT_DIR.is_dir(), (
        f"Directory {AUDIT_DIR} is missing. "
        "The workspace root must exist before students begin."
    )
    assert SAMPLE_DIR.is_dir(), (
        f"Directory {SAMPLE_DIR} is missing. "
        "The provided sample_data/ directory must exist."
    )


def test_sample_files_exist_and_content():
    for f in (FILE1, FILE2):
        assert f.is_file(), f"Required sample file {f} is missing."

    # file1.txt must be empty
    size_file1 = FILE1.stat().st_size
    assert size_file1 == 0, (
        f"{FILE1} should be empty (0 bytes) but is {size_file1} bytes."
    )

    # file2.txt must contain exactly b"abc"
    data2 = FILE2.read_bytes()
    assert data2 == b"abc", (
        f"{FILE2} should contain ASCII 'abc' with no newline. "
        f"Found {len(data2)} bytes: {data2!r}"
    )

    # Ensure no unexpected extra regular files in sample_data/
    regular_files = sorted(
        p.relative_to(SAMPLE_DIR) for p in SAMPLE_DIR.rglob("*") if p.is_file()
    )
    assert regular_files == [Path("file1.txt"), Path("file2.txt")], (
        f"sample_data/ should contain only file1.txt and file2.txt. "
        f"Found: {', '.join(map(str, regular_files)) or 'no files'}"
    )


def test_sample_file_hashes():
    mismatches = []
    for path, expected_digest in EXPECTED_SHA256.items():
        digest = sha256_hex(path)
        if digest != expected_digest:
            mismatches.append(f"{path} => {digest} (expected {expected_digest})")

    assert not mismatches, (
        "SHA-256 digest mismatch for the following file(s):\n" +
        "\n".join(mismatches)
    )


def test_makefile_not_present_yet():
    assert not MAKEFILE_PATH.exists(), (
        f"{MAKEFILE_PATH} already exists. "
        "The Makefile should be created by the student, "
        "so it must not be present in the starter repository."
    )


def test_output_files_absent():
    unexpected = [p for p in OUTPUT_FILES if p.exists()]
    assert not unexpected, (
        "The following output artefact(s) already exist even though no "
        "student action has occurred:\n" +
        "\n".join(map(str, unexpected))
    )