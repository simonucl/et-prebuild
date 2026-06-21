# test_initial_state.py
#
# Pytest suite that validates the _initial_ filesystem state **before**
# the student performs any action for the “connectivity assessment” task.
#
# Requirements checked:
# 1. /home/user/targets.txt
#    • file exists, is a regular readable file
#    • contains exactly the three expected lines, in order
#    • each line is terminated by a single LF (`\n`) character
#
# NOTE:
# • We intentionally do *not* test for the presence or absence of any
#   other files or directories (e.g. /home/user/connectivity_check.sh,
#   /home/user/logs, /home/user/logs/connectivity_report.log) because
#   they are artefacts that will be created by the student’s solution.
# • Only the Python standard library and pytest are used.


import os
from pathlib import Path
import stat
import pytest

TARGETS_FILE = Path("/home/user/targets.txt")

EXPECTED_LINES = [
    "127.0.0.1\n",
    "localhost\n",
    "198.51.100.1\n",
]


def _read_targets_file():
    """
    Helper that opens /home/user/targets.txt in text mode with universal
    newline support disabled so we can verify exact LF terminators.
    """
    # Explicitly disable universal newlines (`newline=""`) so Python does
    # not perform any newline translation; this lets us see the real bytes.
    with TARGETS_FILE.open("r", encoding="utf-8", newline="") as fp:
        return fp.readlines()


def test_targets_file_exists_and_regular():
    """Ensure /home/user/targets.txt exists and is a regular file."""
    assert TARGETS_FILE.exists(), (
        f"Expected {TARGETS_FILE} to exist but it does not."
    )
    assert TARGETS_FILE.is_file(), (
        f"Expected {TARGETS_FILE} to be a regular file."
    )

    # Readability: the user running pytest should have at least one of the
    # read permission bits (u, g, or o). We test this via os.access.
    assert os.access(TARGETS_FILE, os.R_OK), (
        f"{TARGETS_FILE} exists but is not readable."
    )

    # Also verify it is not a symlink or other special file.
    mode = TARGETS_FILE.stat().st_mode
    assert stat.S_ISREG(mode), (
        f"{TARGETS_FILE} is not a regular file (mode: {oct(mode)})."
    )


def test_targets_file_exact_contents():
    """
    Validate that the file has exactly three lines, in order, each
    terminated by a single LF and with no trailing whitespace.
    """
    lines = _read_targets_file()

    # Verify line count first for a clearer error message if it fails.
    assert len(lines) == 3, (
        f"{TARGETS_FILE} should contain exactly 3 lines, "
        f"but it contains {len(lines)} lines."
    )

    # Check each expected line matches exactly.
    for idx, (expected, actual) in enumerate(zip(EXPECTED_LINES, lines), start=1):
        assert actual == expected, (
            f"Line {idx} of {TARGETS_FILE} is incorrect.\n"
            f"  Expected: {expected!r}\n"
            f"  Found   : {actual!r}"
        )

    # Sanity check: final byte of the file is LF.
    with TARGETS_FILE.open("rb") as fp:
        fp.seek(-1, os.SEEK_END)
        last_byte = fp.read(1)
    assert last_byte == b"\n", (
        f"{TARGETS_FILE} must end with a single LF (\\n) character."
    )