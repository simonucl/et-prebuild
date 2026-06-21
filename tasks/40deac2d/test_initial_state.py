# test_initial_state.py
#
# Pytest suite that verifies the *initial* sandbox state for the
# “backup-and-restore” exercise.  These checks run **before** the student
# performs any action.
#
# Rules enforced by this test file:
#   • The only pre-existing data must be the folder
#       /home/user/backup_demo/original/
#     containing the single file sample.txt.
#   • The file must contain exactly the five ASCII bytes “hello”
#     with *no* trailing newline and must match the expected SHA-256 hash.
#
# NOTE:
#   We intentionally do NOT test for the presence or absence of any of the
#   required *output* artefacts (backup/, restore/, backup.tar.gz, log file,
#   etc.) because those will be created by the student later.  The developer
#   instructions forbid such checks in the initial-state test suite.
#
# Only Python stdlib and pytest are used.

import hashlib
import os
from pathlib import Path

# Constants ---------------------------------------------------------------

BASE_DIR = Path("/home/user/backup_demo")
ORIGINAL_DIR = BASE_DIR / "original"
SAMPLE_FILE = ORIGINAL_DIR / "sample.txt"
EXPECTED_CONTENT = b"hello"  # 5 bytes, no trailing newline
EXPECTED_SHA256 = (
    "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
)


# Helper ------------------------------------------------------------------

def sha256_of_file(path: Path) -> str:
    """Return the hex-encoded SHA-256 digest of the given file."""
    hasher = hashlib.sha256()
    with path.open("rb") as fp:
        for chunk in iter(lambda: fp.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


# Tests -------------------------------------------------------------------

def test_base_directory_exists():
    assert BASE_DIR.is_dir(), (
        f"Expected base directory {BASE_DIR} to exist, "
        "but it is missing."
    )


def test_original_directory_exists():
    assert ORIGINAL_DIR.is_dir(), (
        f"Expected original directory {ORIGINAL_DIR} to exist, "
        "but it is missing."
    )


def test_sample_file_exists_and_is_file():
    assert SAMPLE_FILE.exists(), (
        f"Expected file {SAMPLE_FILE} to exist, but it is missing."
    )
    assert SAMPLE_FILE.is_file(), (
        f"{SAMPLE_FILE} exists but is not a regular file."
    )


def test_sample_file_content_and_hash():
    # Check file size and exact content.
    data = SAMPLE_FILE.read_bytes()
    assert data == EXPECTED_CONTENT, (
        f"{SAMPLE_FILE} content mismatch. "
        f"Expected exactly {EXPECTED_CONTENT!r} "
        f"(ascii 'hello' with no newline) but got {data!r}."
    )
    assert len(data) == 5, (
        f"{SAMPLE_FILE} should be 5 bytes but is {len(data)} bytes long."
    )

    # Check SHA-256 hash.
    computed_hash = sha256_of_file(SAMPLE_FILE)
    assert computed_hash == EXPECTED_SHA256, (
        f"SHA-256 mismatch for {SAMPLE_FILE}.\n"
        f"Expected: {EXPECTED_SHA256}\n"
        f"Found:    {computed_hash}"
    )