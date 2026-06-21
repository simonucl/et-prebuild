# test_initial_state.py
#
# Pytest suite that validates the *initial* on-disk state **before**
# the learner begins the exercise described in the task.  These tests
# purposefully verify only the pre-task conditions; they do **not**
# check for the existence or correctness of any artefact that the
# learner is expected to create later (e.g. extension_frequency.log).
#
# If any assertion here fails, the exercise is not starting from the
# required clean slate and the learner must not continue.

import os
import stat
from pathlib import Path

import pytest


# ---------- Constants ---------------------------------------------------------

DISK_USAGE_DIR = Path("/home/user/disk_usage")
RAW_LIST_FILE = DISK_USAGE_DIR / "raw_file_list.txt"
OUTPUT_FILE   = DISK_USAGE_DIR / "extension_frequency.log"

EXPECTED_LINES = [
    ".log",
    ".tmp",
    ".log",
    ".bak",
    ".log",
    ".txt",
    ".tmp",
    ".csv",
    ".csv",
    ".txt",
    ".log",
    ".bak",
    ".iso",
    ".iso",
    ".tmp",
    ".log",
    ".img",
]

DIR_MODE_EXPECTED  = 0o755
FILE_MODE_EXPECTED = 0o644


# ---------- Helper utilities --------------------------------------------------

def _mode_bits(path: Path) -> int:
    """
    Return the permission bits (as an int) of `path` in the customary
    0o755 / 0o644 notation, masking out file-type bits.
    """
    return stat.S_IMODE(path.stat().st_mode)


def _format_mode(mode_int: int) -> str:
    """Return a human-readable 3-digit octal string for error messages."""
    return oct(mode_int)[-3:]


# ---------- Tests -------------------------------------------------------------

def test_disk_usage_directory_exists_and_mode():
    assert DISK_USAGE_DIR.exists(), (
        f"Required directory {DISK_USAGE_DIR} is missing."
    )
    assert DISK_USAGE_DIR.is_dir(), (
        f"{DISK_USAGE_DIR} exists but is not a directory."
    )

    actual_mode = _mode_bits(DISK_USAGE_DIR)
    assert actual_mode == DIR_MODE_EXPECTED, (
        f"{DISK_USAGE_DIR} must have mode "
        f"{_format_mode(DIR_MODE_EXPECTED)} "
        f"but has {_format_mode(actual_mode)}."
    )


def test_raw_file_list_exists_mode_and_content():
    # Presence & type ----------------------------------------------------------
    assert RAW_LIST_FILE.exists(), (
        f"Source file {RAW_LIST_FILE} is missing."
    )
    assert RAW_LIST_FILE.is_file(), (
        f"{RAW_LIST_FILE} exists but is not a regular file."
    )

    # Permissions --------------------------------------------------------------
    actual_mode = _mode_bits(RAW_LIST_FILE)
    assert actual_mode == FILE_MODE_EXPECTED, (
        f"{RAW_LIST_FILE} must have mode "
        f"{_format_mode(FILE_MODE_EXPECTED)} "
        f"but has {_format_mode(actual_mode)}."
    )

    # Exact content ------------------------------------------------------------
    with RAW_LIST_FILE.open("r", encoding="utf-8") as fh:
        content = fh.read().splitlines(keepends=False)

    assert content == EXPECTED_LINES, (
        f"Content of {RAW_LIST_FILE} does not match the expected "
        f"{len(EXPECTED_LINES)} lines.\n"
        f"Expected:\n{EXPECTED_LINES}\n\n"
        f"Found:\n{content}"
    )


def test_no_output_file_yet():
    assert not OUTPUT_FILE.exists(), (
        f"{OUTPUT_FILE} should NOT exist before the student runs their "
        f"solution, but it is already present."
    )


def test_no_extra_files_present():
    """
    The working directory must contain exactly one file (raw_file_list.txt)
    and nothing else at this point.
    """
    entries = [p.name for p in DISK_USAGE_DIR.iterdir() if p.is_file()]
    assert entries == ["raw_file_list.txt"], (
        f"{DISK_USAGE_DIR} contains unexpected files at the outset: {entries}. "
        "Only 'raw_file_list.txt' should be present."
    )