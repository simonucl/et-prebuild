# test_initial_state.py
#
# This pytest file validates that the operating-system / filesystem
# is in the expected *initial* state BEFORE the learner performs any
# actions for the “DNS restore drill” exercise.
#
# We deliberately DO NOT look for any artefacts that the learner must
# create (/home/user/restore_tests, copied files, log files, …).
#
# Only standard-library modules plus pytest are used.

import os
import re
import stat
import pytest

# ---------------------------------------------------------------------------
# CONSTANTS ‑ full, absolute paths only
# ---------------------------------------------------------------------------
SOURCE_FILE = "/home/user/mock_dns/hosts_mapping"
SOURCE_DIR = "/home/user/mock_dns"
RESTORE_DIR = "/home/user/restore_tests"
RESTORE_FILE = "/home/user/restore_tests/hosts_mapping"
LOG_FILE = "/home/user/restore_tests/dns_restore.log"

EXPECTED_LINES = [
    "backup1.example.com 192.168.10.11\n",
    "backup2.example.com 192.168.10.12\n",
    "db1.internal.local 10.0.0.21\n",
    "db2.internal.local 10.0.0.22\n",
]


# ---------------------------------------------------------------------------
# Helper(s)
# ---------------------------------------------------------------------------
ipv4_re = (
    r"(25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\."
    r"(25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\."
    r"(25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\."
    r"(25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)"
)
LINE_PATTERN = re.compile(rf"^[^\s]+\s{ipv4_re}\n$")


# ---------------------------------------------------------------------------
# Tests for the pre-exercise state
# ---------------------------------------------------------------------------
def test_mock_dns_directory_exists_and_is_directory():
    assert os.path.exists(
        SOURCE_DIR
    ), f"Required directory {SOURCE_DIR!r} is missing."
    assert os.path.isdir(
        SOURCE_DIR
    ), f"Expected {SOURCE_DIR!r} to be a directory."


def test_hosts_mapping_file_exists_and_is_regular_file():
    assert os.path.exists(
        SOURCE_FILE
    ), f"Required file {SOURCE_FILE!r} is missing."
    assert os.path.isfile(
        SOURCE_FILE
    ), f"{SOURCE_FILE!r} exists but is not a regular file."


def test_hosts_mapping_file_permissions_read_only():
    mode = stat.S_IMODE(os.stat(SOURCE_FILE).st_mode)
    # The truth value says 0644; we allow *at most* owner-write and world-read.
    expected_mode = 0o644
    assert (
        mode == expected_mode
    ), f"{SOURCE_FILE!r} should have permissions 0644, found {oct(mode)}."


def test_hosts_mapping_file_contents_exact_match():
    with open(SOURCE_FILE, encoding="utf-8") as fp:
        contents = fp.readlines()

    assert (
        contents == EXPECTED_LINES
    ), (
        f"{SOURCE_FILE} contents do not match the expected 4-line reference.\n"
        f"Expected lines:\n{''.join(EXPECTED_LINES)}\n"
        f"Actual lines:\n{''.join(contents)}"
    )

    # Additionally validate each individual line structurally
    for idx, line in enumerate(contents, start=1):
        assert LINE_PATTERN.match(
            line
        ), f"Line {idx} in {SOURCE_FILE} is malformed: {line!r}"


def test_restore_directory_does_not_exist_yet():
    """
    The working directory that the learner will create should NOT exist
    prior to running the learner's solution.
    """
    assert not os.path.exists(
        RESTORE_DIR
    ), (
        f"The directory {RESTORE_DIR!r} already exists before the exercise "
        "starts. It should be created by the learner."
    )


def test_no_copied_file_or_log_file_exist_yet():
    """
    Neither the copied hosts_mapping nor the dns_restore.log file should be
    present before the learner begins work.
    """
    assert not os.path.exists(
        RESTORE_FILE
    ), f"Unexpected pre-existing file {RESTORE_FILE!r} found."
    assert not os.path.exists(
        LOG_FILE
    ), f"Unexpected pre-existing file {LOG_FILE!r} found."