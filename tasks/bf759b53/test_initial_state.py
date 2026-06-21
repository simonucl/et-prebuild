# test_initial_state.py
#
# Pytest suite that validates the operating-system state BEFORE the student’s
# solution code is executed.  It ensures that:
#
#   1. The raw host list exists at the exact absolute path required by
#      the assignment and contains the expected data.
#   2. The output file that the student is supposed to create does *not* yet
#      exist—preventing false-positive grading due to leftover artefacts.
#
# Only the Python standard library and pytest are used.

import os
from pathlib import Path

import pytest

# Absolute paths mandated by the task description
HOSTS_FILE = Path("/home/user/provisioning/hosts.txt")
FREQUENCY_LOG = Path("/home/user/provisioning/host_frequencies.log")

# The ground-truth contents of hosts.txt before the student starts.
# NOTE: A trailing newline after the last line is intentional and verified.
EXPECTED_HOSTS_CONTENT = (
    "web01\n"
    "db01\n"
    "web01\n"
    "web02\n"
    "db01\n"
    "app01\n"
    "web02\n"
    "web02\n"
    "db01\n"
)


def test_hosts_file_exists_and_contains_expected_data():
    """
    The raw input file must be present and contain exactly the known lines.
    This guarantees the starting data set is correct before the student's
    commands run.
    """
    assert HOSTS_FILE.exists(), (
        f"Required input file not found: {HOSTS_FILE}. "
        "The provisioning script cannot proceed without it."
    )

    assert HOSTS_FILE.is_file(), (
        f"Expected a regular file at {HOSTS_FILE}, but something else exists."
    )

    # Read & compare full file contents, including final newline
    actual_content = HOSTS_FILE.read_text(encoding="utf-8")
    assert actual_content == EXPECTED_HOSTS_CONTENT, (
        "The contents of hosts.txt do not match the expected initial dataset.\n\n"
        f"Expected:\n{EXPECTED_HOSTS_CONTENT!r}\n\n"
        f"Got:\n{actual_content!r}"
    )


def test_frequency_log_not_yet_present():
    """
    The summary file must not exist before the student performs any action.
    Its presence would indicate that the environment is already polluted
    and could mask errors in the student's solution.
    """
    assert not FREQUENCY_LOG.exists(), (
        f"Output file {FREQUENCY_LOG} already exists before the task begins. "
        "Please remove it so the student can generate it from scratch."
    )