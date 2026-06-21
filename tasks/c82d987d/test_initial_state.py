# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / file-system
# state **before** the student starts working on the task.  It only checks
# for resources that must exist prior to any action taken by the student
# and explicitly avoids looking for the artefacts the student is expected
# to create later (e.g. /home/user/support, diag_report.txt, tarballs, …).

import os
import stat
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# Constants describing the required pre-existing resources
# --------------------------------------------------------------------------- #

LOG_DIR = Path("/home/user/app/logs")
LOG_FILE = LOG_DIR / "app.log"

EXPECTED_LOG_DIR_MODE = 0o755
EXPECTED_LOG_FILE_MODE = 0o644

EXPECTED_LOG_CONTENT = [
    "2023-01-01 00:00:00 INFO Application started\n",
    "2023-01-01 00:05:00 WARN No config file, using defaults\n",
    "2023-01-01 00:10:00 INFO Service listening on port 8080\n",
]


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _get_perm_bits(path: Path) -> int:
    """
    Return the Unix permission bits (e.g. 0o755) of *path*, stripped of the
    file-type bits.
    """
    return stat.S_IMODE(path.stat().st_mode)


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #

def test_log_directory_exists_and_has_correct_permissions():
    """
    The directory /home/user/app/logs must exist *before* the student acts,
    and it must have permissions 755.
    """
    assert LOG_DIR.is_dir(), (
        f"Required directory not found: {LOG_DIR}. "
        "It should be present before the diagnostic script is run."
    )

    mode = _get_perm_bits(LOG_DIR)
    assert mode == EXPECTED_LOG_DIR_MODE, (
        f"Directory {LOG_DIR} exists but has incorrect permissions "
        f"{oct(mode)}; expected {oct(EXPECTED_LOG_DIR_MODE)}."
    )


def test_log_file_exists_and_has_correct_permissions():
    """
    The file /home/user/app/logs/app.log must exist and have permissions 644
    prior to any student action.
    """
    assert LOG_FILE.is_file(), (
        f"Required log file not found: {LOG_FILE}. "
        "This file is needed so the student can copy it into the support bundle."
    )

    mode = _get_perm_bits(LOG_FILE)
    assert mode == EXPECTED_LOG_FILE_MODE, (
        f"File {LOG_FILE} has incorrect permissions {oct(mode)}; "
        f"expected {oct(EXPECTED_LOG_FILE_MODE)}."
    )


def test_log_file_contents_exact_match():
    """
    Verify that app.log contains exactly the expected three lines and that
    the final line terminates with a newline character.
    """
    with LOG_FILE.open("r", encoding="utf-8") as fh:
        content = fh.readlines()

    assert content == EXPECTED_LOG_CONTENT, (
        f"Contents of {LOG_FILE} do not match the expected diagnostic seed "
        f"data.\nExpected:\n{''.join(EXPECTED_LOG_CONTENT)}\n"
        f"Found:\n{''.join(content)}"
    )