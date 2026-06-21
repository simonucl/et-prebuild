# test_initial_state.py
#
# Pytest suite that validates the initial operating-system / filesystem
# state **before** the learner starts working on the assignment.
#
# What we check:
#   1. The directory /home/user/security_scan/ exists.
#   2. The file  /home/user/security_scan/scan_results.log exists.
#   3. The file contains exactly the seven expected lines (LF-terminated).
#
# We explicitly DO NOT look for the output file the learner is supposed
# to create, in accordance with the grading-infrastructure rules.

import os
from pathlib import Path

import pytest

# ---------- constants ---------------------------------------------------------

SCAN_DIR = Path("/home/user/security_scan")
SCAN_FILE = SCAN_DIR / "scan_results.log"

EXPECTED_LINES = [
    "/var/www/html/index.php -rw-r--r-- root\n",
    "/etc/passwd -rw-r--r-- root\n",
    "/tmp/tempfile.sh -rwxrwxrwx user\n",
    "/home/user/public_notes.txt -rw-rw-r-- user\n",
    "/var/log/app.log -rw-r----- syslog\n",
    "/home/user/scripts/run.sh -rwxr-xr-x user\n",
    "/opt/software/config.cfg -rw-rw-rw- user\n",
]

# ---------- tests -------------------------------------------------------------


def test_scan_directory_exists():
    """Ensure /home/user/security_scan exists and is a directory."""
    assert SCAN_DIR.exists(), (
        f"Required directory {SCAN_DIR} is missing. "
        "The assignment cannot start without it."
    )
    assert SCAN_DIR.is_dir(), f"{SCAN_DIR} exists but is not a directory."


def test_scan_results_file_exists():
    """Ensure scan_results.log exists and is a regular file."""
    assert SCAN_FILE.exists(), (
        f"Required file {SCAN_FILE} is missing. "
        "The learner needs this file to parse the scan results."
    )
    assert SCAN_FILE.is_file(), f"{SCAN_FILE} exists but is not a regular file."


def test_scan_results_content():
    """
    The log file must contain exactly the expected seven lines, each LF-terminated.

    Explanation of the checks:
      * Exact number of lines.
      * Exact byte-for-byte content to avoid hidden whitespace issues.
      * Each line is absolute-path-first (starts with '/').
    """
    with SCAN_FILE.open("r", encoding="utf-8", newline="") as fh:
        actual_lines = fh.readlines()

    assert (
        actual_lines == EXPECTED_LINES
    ), (
        "The contents of scan_results.log do not match the expected initial state.\n"
        f"Expected {len(EXPECTED_LINES)} specific lines:\n{''.join(EXPECTED_LINES)}\n"
        f"Found ({len(actual_lines)} lines):\n{''.join(actual_lines)}"
    )

    # Additional sanity: every line should start with an absolute path.
    for idx, line in enumerate(actual_lines, start=1):
        assert line.startswith(
            "/"
        ), f"Line {idx} of {SCAN_FILE} does not start with '/': {line!r}"