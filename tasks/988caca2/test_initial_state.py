# test_initial_state.py
#
# Pytest suite that validates the *initial* OS / filesystem state
# before the student performs any action for the “package-archive”
# exercise.
#
# Rules respected:
#   • Uses only the Python standard library + pytest.
#   • Tests only the pre-existing snapshot, **not** the deliverables
#     that the student must create (/home/user/backups/…).
#   • Uses absolute paths for all filesystem checks.
#   • Provides clear failure messages to help diagnose missing or
#     malformed prerequisites.

import os
import stat
import re
import pytest

SNAPSHOT_DIR = "/home/user/data"
SNAPSHOT_FILE = os.path.join(SNAPSHOT_DIR, "dpkg_status_snapshot.txt")

EXPECTED_LINES = {
    "coreutils 8.32-4.1",
    "bash 5.1-2",
    "grep 3.6-1",
    "dpkg 1.20.9",
    "sed 4.8-1",
}

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------


def _is_regular_file(path: str) -> bool:
    """Return True if *path* exists and is a regular file."""
    try:
        return stat.S_ISREG(os.stat(path).st_mode)
    except FileNotFoundError:
        return False


def _read_snapshot_lines(path: str):
    """Read non-empty lines from *path*, stripped of trailing newlines."""
    with open(path, "rt", encoding="utf-8") as fh:
        return [ln.rstrip("\n") for ln in fh if ln.strip()]


# ----------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------


def test_snapshot_directory_exists_and_is_dir():
    assert os.path.isdir(
        SNAPSHOT_DIR
    ), f"Required directory {SNAPSHOT_DIR!r} is missing or not a directory."


def test_snapshot_file_exists_and_is_regular():
    assert _is_regular_file(
        SNAPSHOT_FILE
    ), f"Required snapshot file {SNAPSHOT_FILE!r} is missing or not a regular file."


def test_snapshot_file_has_expected_content():
    # 1. Read & basic sanity check
    lines = _read_snapshot_lines(SNAPSHOT_FILE)

    assert (
        len(lines) == 5
    ), f"Snapshot file should contain exactly 5 non-blank lines; found {len(lines)}."

    # 2. Line-format validation: "<package_name> <version>"
    bad_format = [
        ln for ln in lines if not re.fullmatch(r"[^\s]+ \S+", ln)
    ]  # exactly one space
    assert (
        not bad_format
    ), f"These lines do not match the expected 'pkg version' format: {bad_format}"

    # 3. Content validation (order is not checked here)
    missing = EXPECTED_LINES.difference(lines)
    extra = set(lines).difference(EXPECTED_LINES)

    assert (
        not missing
    ), f"Snapshot file is missing the following expected entries: {sorted(missing)}"
    assert (
        not extra
    ), f"Snapshot file contains unexpected entries: {sorted(extra)}"