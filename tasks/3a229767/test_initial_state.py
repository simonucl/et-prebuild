# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem
# state before the student performs any actions for the “artifact-repository
# curator” task.
#
# Rules enforced:
#   • /home/user/repos must exist and be a directory.
#   • /home/user/repos/scan_2023-07-01.log must exist and contain the exact
#     10 lines (including two duplicate pairs) specified in the task
#     description.
#   • /home/user/output must *not* exist yet.
#
# Only stdlib + pytest are used.


import os
import stat
import pytest
from pathlib import Path

REPOS_DIR = Path("/home/user/repos")
SCAN_LOG = REPOS_DIR / "scan_2023-07-01.log"
OUTPUT_DIR = Path("/home/user/output")

# The lines exactly as given in the task description (order matters)
EXPECTED_SCAN_LINES = [
    "central|libalpha|2.1.0|x86_64|e1b71a5",
    "central|libalpha|2.1.0|x86_64|e1b71a5",
    "central|libalpha|2.3.1|arm64|a2c903f",
    "central|libbeta|1.4.2|x86_64|ff3be91",
    "central|toolset|5.0.0|x86_64|4abff29",
    "local|libalpha|2.3.1|x86_64|b1c223d",
    "local|libgamma|0.9.8|arm64|6d904aa",
    "remote|libbeta|2.0.0|x86_64|7ea29fe",
    "remote|toolset|5.1.1|arm64|c8d0aa7",
    "remote|toolset|5.1.1|arm64|c8d0aa7",
]


def _perm_bits(path: Path):
    """Return permission bits similar to ls -l (octal 0o755, etc.)."""
    return stat.S_IMODE(path.stat().st_mode)


def test_repos_directory_exists_and_permissions():
    assert REPOS_DIR.exists(), (
        f"Expected directory {REPOS_DIR} to exist, but it is missing."
    )
    assert REPOS_DIR.is_dir(), (
        f"Expected {REPOS_DIR} to be a directory, but it is not."
    )

    # Basic permission sanity: at least owner read/write/execute
    mode = _perm_bits(REPOS_DIR)
    assert mode & 0o700 == 0o700, (
        f"Directory {REPOS_DIR} should be accessible to the owner (rwx); "
        f"found permissions {oct(mode)}."
    )


def test_scan_log_exists_and_permissions():
    assert SCAN_LOG.exists(), (
        f"Expected file {SCAN_LOG} to exist, but it is missing."
    )
    assert SCAN_LOG.is_file(), (
        f"Expected {SCAN_LOG} to be a regular file."
    )

    mode = _perm_bits(SCAN_LOG)
    assert mode & 0o600 == 0o600, (
        f"File {SCAN_LOG} must be readable and writable by owner; "
        f"found permissions {oct(mode)}."
    )


def test_scan_log_contents_exact():
    with SCAN_LOG.open("r", encoding="utf-8") as fh:
        raw_lines = fh.readlines()

    # Strip only the trailing newline; internal whitespace must match exactly
    lines = [line.rstrip("\n") for line in raw_lines]

    assert lines, f"{SCAN_LOG} appears to be empty."

    # 1) Exact number of lines
    assert len(lines) == 10, (
        f"Expected 10 lines in {SCAN_LOG}; found {len(lines)}."
    )

    # 2) Exact order / content match
    assert lines == EXPECTED_SCAN_LINES, (
        f"The contents of {SCAN_LOG} do not match the expected initial data.\n"
        f"--- Expected (first 10 shown)\n{EXPECTED_SCAN_LINES}\n"
        f"--- Actual   (first 10 shown)\n{lines[:10]}"
    )

    # 3) Validate duplicate pairs explicitly for pedagogical clarity
    dup1_ok = lines[0] == lines[1]
    dup2_ok = lines[8] == lines[9]
    assert dup1_ok and dup2_ok, (
        "Duplicate line pairs are not present as expected:\n"
        f"  lines[0] = {lines[0]!r}\n"
        f"  lines[1] = {lines[1]!r}\n"
        f"  lines[8] = {lines[8]!r}\n"
        f"  lines[9] = {lines[9]!r}"
    )


def test_output_directory_absent():
    assert not OUTPUT_DIR.exists(), (
        f"The directory {OUTPUT_DIR} should NOT exist before processing begins."
    )