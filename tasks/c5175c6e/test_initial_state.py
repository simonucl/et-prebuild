# test_initial_state.py
#
# This test-suite validates that the *initial* operating-system / filesystem
# state exactly matches the specification given to the student **before**
# they perform any actions.  It intentionally avoids touching or asserting
# about any of the output artefacts that the student is expected to create
# later on (e.g., /home/user/ci_cd/reports/**).

import os
import stat
from pathlib import Path

import pytest

HOME = Path("/home/user")
LOG_DIR = HOME / "ci_cd" / "logs"
LOG_FILE = LOG_DIR / "build.log"

EXPECTED_LOG_PERMS = 0o600
EXPECTED_DIR_PERMS = 0o700

EXPECTED_LOG_LINES = [
    "2023-06-01T10:30:25Z Build #101 SUCCESS\n",
    "2023-06-01T11:00:20Z Build #102 FAILED\n",
    "2023-06-01T11:30:42Z Build #103 SUCCESS\n",
    "2023-06-01T12:00:05Z Build #104 SUCCESS\n",
    "2023-06-01T12:30:44Z Build #105 ABORTED\n",
    "2023-06-01T13:00:22Z Build #106 FAILED\n",
    "2023-06-01T13:30:51Z Build #107 SUCCESS\n",
    "2023-06-01T14:00:30Z Build #108 FAILED\n",
    "2023-06-01T14:30:25Z Build #109 FAILED\n",
    "2023-06-01T15:00:40Z Build #110 ABORTED\n",
    "2023-06-01T15:30:15Z Build #111 SUCCESS\n",
]


def _friendly_perm(octal_value: int) -> str:
    """Return a string like '0o700' for display purposes."""
    return oct(octal_value)


def test_logs_directory_exists_and_has_correct_permissions():
    assert LOG_DIR.exists(), (
        f"Required directory {LOG_DIR} is missing. "
        "The initial environment must contain this directory."
    )
    assert LOG_DIR.is_dir(), f"{LOG_DIR} exists but is not a directory."
    perms = stat.S_IMODE(os.stat(LOG_DIR).st_mode)
    assert perms == EXPECTED_DIR_PERMS, (
        f"{LOG_DIR} permissions are {_friendly_perm(perms)}; "
        f"expected {_friendly_perm(EXPECTED_DIR_PERMS)} (rwx------)."
    )


def test_build_log_exists_and_has_correct_permissions():
    assert LOG_FILE.exists(), (
        f"Required file {LOG_FILE} is missing. "
        "The initial environment must contain this file."
    )
    assert LOG_FILE.is_file(), f"{LOG_FILE} exists but is not a regular file."
    perms = stat.S_IMODE(os.stat(LOG_FILE).st_mode)
    assert perms == EXPECTED_LOG_PERMS, (
        f"{LOG_FILE} permissions are {_friendly_perm(perms)}; "
        f"expected {_friendly_perm(EXPECTED_LOG_PERMS)} (rw-------)."
    )


def test_build_log_has_expected_content():
    with LOG_FILE.open("r", encoding="utf-8") as fh:
        actual_lines = fh.readlines()

    assert actual_lines == EXPECTED_LOG_LINES, (
        f"The contents of {LOG_FILE} do not match the expected initial state.\n\n"
        "Expected:\n"
        + "".join(EXPECTED_LOG_LINES)
        + "\nActual:\n"
        + "".join(actual_lines)
    )