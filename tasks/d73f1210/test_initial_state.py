# test_initial_state.py
#
# Pytest suite that verifies the pre-existing filesystem state *before*
# the student runs their single find | sort | xargs command.
#
# The checks confirm that:
#   1. Required directories exist.
#   2. Incoming directory contains exactly the expected files.
#   3. Archive directory exists but is completely empty.
#   4. No move.log file is present yet.
#   5. Initial files have the expected contents.
#
# Only the Python stdlib and pytest are used.

import os
from pathlib import Path

WORKFLOW_DIR = Path("/home/user/workflow")
INCOMING_DIR = WORKFLOW_DIR / "incoming"
ARCHIVE_DIR = WORKFLOW_DIR / "archive"
MOVE_LOG = WORKFLOW_DIR / "move.log"

EXPECTED_INCOMING_FILES = {
    "january.dat": b"JAN DATA\n",
    "february.dat": b"FEB DATA\n",
    "march.dat": b"MAR DATA\n",
    "readme.txt": b"Put data files here.\n",
}


def _read_bytes(path: Path) -> bytes:
    """Helper that reads a file in binary mode."""
    with path.open("rb") as fh:
        return fh.read()


def test_directories_exist():
    """The workflow, incoming and archive directories must all exist."""
    assert WORKFLOW_DIR.is_dir(), (
        f"Required directory {WORKFLOW_DIR} does not exist."
    )
    assert INCOMING_DIR.is_dir(), (
        f"Required directory {INCOMING_DIR} does not exist."
    )
    assert ARCHIVE_DIR.is_dir(), (
        f"Required directory {ARCHIVE_DIR} does not exist."
    )


def test_incoming_contains_expected_files_only():
    """
    /incoming/ must contain *exactly* the four expected files:
    january.dat, february.dat, march.dat and readme.txt.
    """
    present_files = {p.name for p in INCOMING_DIR.iterdir() if p.is_file()}
    expected_files = set(EXPECTED_INCOMING_FILES.keys())
    missing = expected_files - present_files
    extra = present_files - expected_files

    assert not missing, (
        f"The following expected file(s) are missing in {INCOMING_DIR}: {', '.join(sorted(missing))}"
    )
    assert not extra, (
        f"The following unexpected file(s) are present in {INCOMING_DIR}: {', '.join(sorted(extra))}"
    )


def test_incoming_file_contents():
    """
    Each initial file must have the exact byte-for-byte content defined
    in EXPECTED_INCOMING_FILES.
    """
    for filename, expected_bytes in EXPECTED_INCOMING_FILES.items():
        path = INCOMING_DIR / filename
        assert path.is_file(), (
            f"Expected {path} to exist, but it does not."
        )
        actual_bytes = _read_bytes(path)
        assert actual_bytes == expected_bytes, (
            f"File {path} has unexpected content.\n"
            f"Expected: {expected_bytes!r}\n"
            f"Actual:   {actual_bytes!r}"
        )


def test_archive_is_empty():
    """/archive/ must exist and be completely empty."""
    contents = list(ARCHIVE_DIR.iterdir())
    assert not contents, (
        f"{ARCHIVE_DIR} is expected to be empty before the task runs, "
        f"but it contains: {', '.join(p.name for p in contents)}"
    )


def test_move_log_does_not_exist_yet():
    """move.log must not exist before the student runs their command."""
    assert not MOVE_LOG.exists(), (
        f"{MOVE_LOG} should NOT exist yet; it will be created by the student's command."
    )