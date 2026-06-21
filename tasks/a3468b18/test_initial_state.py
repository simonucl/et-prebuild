# test_initial_state.py
"""
Pytest suite that verifies the *initial* state of the filesystem before the
student performs any actions for the checksum-manifest exercise.

Rules being checked:
1. The existing project tree /home/user/project/data/ contains exactly the two
   pre-populated files with the correct contents and SHA-256 digests.
2. The target output directory /home/user/project/checksums/ must *not* exist
   yet (nothing has been created by the student).
"""

import hashlib
from pathlib import Path

PROJECT_ROOT = Path("/home/user/project")
DATA_DIR = PROJECT_ROOT / "data"
CHECKSUMS_DIR = PROJECT_ROOT / "checksums"

FILE1 = DATA_DIR / "file1.txt"
FILE2 = DATA_DIR / "file2.bin"

# Expected raw byte contents
EXPECTED_FILE1_BYTES = b"abc"  # exactly 3 bytes, no newline
EXPECTED_FILE2_BYTES = b"The quick brown fox jumps over the lazy dog"  # 43 bytes

# Corresponding expected SHA-256 digests (hex)
EXPECTED_FILE1_SHA256 = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
EXPECTED_FILE2_SHA256 = "d7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592"


def sha256_of(path: Path) -> str:
    """Return the hex-encoded SHA-256 digest of the file at *path*."""
    h = hashlib.sha256()
    with path.open("rb") as fp:
        for chunk in iter(lambda: fp.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def test_data_directory_exists():
    assert DATA_DIR.is_dir(), (
        f"Required directory {DATA_DIR} is missing. "
        "The grader expects the pre-populated data/ directory to be present."
    )


def test_required_files_exist():
    for f in (FILE1, FILE2):
        assert f.is_file(), (
            f"Required file {f} is missing. "
            "Both data/file1.txt and data/file2.bin must exist before work begins."
        )


def test_file1_contents_and_sha256():
    data = FILE1.read_bytes()
    assert (
        data == EXPECTED_FILE1_BYTES
    ), f"{FILE1} contents differ from the expected 3-byte string 'abc'."

    digest = sha256_of(FILE1)
    assert (
        digest == EXPECTED_FILE1_SHA256
    ), f"{FILE1} SHA-256 mismatch. Expected {EXPECTED_FILE1_SHA256}, got {digest}."


def test_file2_contents_and_sha256():
    data = FILE2.read_bytes()
    assert (
        data == EXPECTED_FILE2_BYTES
    ), f"{FILE2} contents differ from the expected sentence."

    digest = sha256_of(FILE2)
    assert (
        digest == EXPECTED_FILE2_SHA256
    ), f"{FILE2} SHA-256 mismatch. Expected {EXPECTED_FILE2_SHA256}, got {digest}."


def test_checksums_directory_not_present():
    assert not CHECKSUMS_DIR.exists(), (
        f"The directory {CHECKSUMS_DIR} already exists, but it should *not* be present "
        "before the student creates it during the task. Please remove it before grading."
    )