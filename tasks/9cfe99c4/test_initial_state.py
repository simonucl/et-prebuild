# test_initial_state.py
#
# Pytest suite that validates the initial on-disk state before the
# student starts working on the “incident-response” task.
#
# The checks focus EXCLUSIVELY on the source artefacts that must be
# preserved.  Nothing is asserted about the soon-to-be-created output
# locations (/home/user/incident_response, /home/user/sync_logs, etc.),
# in accordance with the grading-suite rules.

import hashlib
import os
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# CONSTANTS
# ---------------------------------------------------------------------------

HOME = Path("/home/user")
SRC_ROOT = HOME / "incident_data_source"
IMAGES_DIR = SRC_ROOT / "images"
LOGS_DIR = SRC_ROOT / "logs"

# Expected files, their sizes and SHA-256 digests
EXPECTED_FILES = {
    IMAGES_DIR / "incident_pic1.jpg": {
        "size": 1,
        "sha256": "ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb",
        "content": b"a",
    },
    IMAGES_DIR / "incident_pic2.png": {
        "size": 3,
        "sha256": "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
        "content": b"abc",
    },
    LOGS_DIR / "app.log": {
        "size": 5,
        "sha256": "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824",
        "content": b"hello",
    },
    LOGS_DIR / "error.log": {
        "size": 4,
        "sha256": "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08",
        "content": b"test",
    },
}

# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def sha256_of_file(path: Path) -> str:
    """Return lowercase hex SHA-256 of the file at *path*."""
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------------------
# TESTS
# ---------------------------------------------------------------------------

def test_root_directories_exist_and_are_directories():
    """Top-level directories must be present and of the correct type."""
    assert SRC_ROOT.exists(), f"Required directory {SRC_ROOT} does not exist."
    assert SRC_ROOT.is_dir(), f"{SRC_ROOT} exists but is not a directory."

    assert IMAGES_DIR.exists(), f"Directory {IMAGES_DIR} is missing."
    assert IMAGES_DIR.is_dir(), f"{IMAGES_DIR} exists but is not a directory."

    assert LOGS_DIR.exists(), f"Directory {LOGS_DIR} is missing."
    assert LOGS_DIR.is_dir(), f"{LOGS_DIR} exists but is not a directory."


def test_no_unexpected_files_present():
    """
    The images/ and logs/ sub-directories must contain EXACTLY the expected
    files and nothing else.
    """
    actual_files = {p for p in SRC_ROOT.rglob("*") if p.is_file()}
    expected_files = set(EXPECTED_FILES.keys())

    missing = expected_files - actual_files
    extras = actual_files - expected_files

    assert not missing, (
        "The following required file(s) are missing:\n"
        + "\n".join(str(p) for p in sorted(missing))
    )
    assert not extras, (
        "Unexpected extra file(s) found in source directory:\n"
        + "\n".join(str(p) for p in sorted(extras))
    )


@pytest.mark.parametrize("path,meta", EXPECTED_FILES.items())
def test_file_size_and_content_and_hash(path: Path, meta: dict):
    """Every expected file must have the correct size, contents and SHA-256."""
    assert path.exists(), f"Expected file {path} is missing."
    assert path.is_file(), f"{path} exists but is not a regular file."

    # Size
    actual_size = path.stat().st_size
    assert (
        actual_size == meta["size"]
    ), f"File {path} should be {meta['size']} byte(s) but is {actual_size}."

    # Content & hash
    actual_content = path.read_bytes()
    assert (
        actual_content == meta["content"]
    ), f"File {path} does not have the expected byte content."

    actual_hash = sha256_of_file(path)
    assert (
        actual_hash == meta["sha256"]
    ), f"SHA-256 mismatch for {path}: expected {meta['sha256']}, got {actual_hash}."


# NOTE:
# We intentionally refrain from testing for the presence OR absence of any
# paths under /home/user/incident_response or /home/user/sync_logs, because
# those are output artefacts that do not concern the initial state.