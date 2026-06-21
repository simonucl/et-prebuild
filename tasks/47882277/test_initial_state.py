# test_initial_state.py
#
# Pytest suite that validates the **initial** operating-system / filesystem
# state *before* the student starts the backup task.

import os
import re
from pathlib import Path

import pytest

HOME = Path("/home/user")
DATA_ROOT = HOME / "data_to_archive"
BACKUPS_ROOT = HOME / "backups"

# --------------------------------------------------------------------------- #
# Helper data                                                                 #
# --------------------------------------------------------------------------- #

EXPECTED_TREE = {
    DATA_ROOT / "docs" / "report1.txt": b"Quarterly Report Q1 2024\n",
    DATA_ROOT / "docs" / "report2.txt": b"Quarterly Report Q2 2024\n",
    DATA_ROOT / "media" / "image1.jpg": b"FAKEJPEGDATA\n",
    DATA_ROOT / "media" / "video1.mp4": b"FAKEMP4DATA\n",
}

TOTAL_EXPECTED_BYTES = sum(len(c) for c in EXPECTED_TREE.values())  # 75
TOTAL_EXPECTED_FILES = len(EXPECTED_TREE)                           # 4


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #

def test_data_directory_exists_and_is_dir():
    """The main data directory must exist and be a directory."""
    assert DATA_ROOT.exists(), f"Expected directory {DATA_ROOT} to exist."
    assert DATA_ROOT.is_dir(), f"{DATA_ROOT} exists but is not a directory."


def test_expected_files_present_with_correct_content():
    """
    Every expected file must exist, be a regular file and contain the exact
    byte sequence specified in the task description.
    """
    for path, expected_bytes in EXPECTED_TREE.items():
        assert path.exists(), f"Missing file: {path}"
        assert path.is_file(), f"Path is not a regular file: {path}"

        actual_bytes = path.read_bytes()
        assert actual_bytes == expected_bytes, (
            f"Content mismatch for {path}.\n"
            f"Expected ({len(expected_bytes)} bytes): {expected_bytes!r}\n"
            f"Actual   ({len(actual_bytes)} bytes): {actual_bytes!r}"
        )


def test_no_extra_files_in_data_directory():
    """
    Only the expected files should be present under /home/user/data_to_archive.
    Other files or directories would make the verification logic ambiguous.
    """
    actual_files = {p for p in DATA_ROOT.rglob("*") if p.is_file()}
    expected_files = set(EXPECTED_TREE.keys())

    extra_files = actual_files - expected_files
    missing_files = expected_files - actual_files

    msg_parts = []
    if missing_files:
        msg_parts.append(f"Missing files: {', '.join(map(str, sorted(missing_files)))}")
    if extra_files:
        msg_parts.append(f"Unexpected files: {', '.join(map(str, sorted(extra_files)))}")

    assert not msg_parts, " | ".join(msg_parts)


def test_expected_totals_match():
    """
    Validate that the total number of files and their combined size match the
    ground-truth used by the final checker.
    """
    actual_total_files = len(EXPECTED_TREE)
    actual_total_bytes = sum((p.read_bytes().__len__() for p in EXPECTED_TREE))

    assert actual_total_files == TOTAL_EXPECTED_FILES, (
        f"Expected {TOTAL_EXPECTED_FILES} files but found {actual_total_files}."
    )
    assert actual_total_bytes == TOTAL_EXPECTED_BYTES, (
        f"Expected {TOTAL_EXPECTED_BYTES} total bytes but found {actual_total_bytes}."
    )


def test_backups_directory_absent():
    """
    The /home/user/backups directory must NOT exist at the initial state.
    Its presence would indicate that the student (or a previous run) already
    produced backup artefacts, violating the clean-slate requirement.
    """
    assert not BACKUPS_ROOT.exists(), (
        f"Directory {BACKUPS_ROOT} should not exist before the backup task starts."
    )


def test_no_preexisting_backup_files_anywhere_under_home():
    """
    Ensure there are no files matching the backup naming scheme anywhere under
    /home/user at the beginning.
    """
    pattern = re.compile(r"^data_backup_\d{8}_\d{4}\.(tar\.gz|sha256|sha256\.gz)$")
    offending_paths = []

    for path in HOME.rglob("*"):
        if path.is_file() and pattern.match(path.name):
            offending_paths.append(path)

    assert not offending_paths, (
        "Found pre-existing backup artefacts (should not be present):\n"
        + "\n".join(map(str, offending_paths))
    )