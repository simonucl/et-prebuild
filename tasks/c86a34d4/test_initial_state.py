# test_initial_state.py
#
# This test-suite verifies that the operating system / filesystem is in the
# expected *initial* state **before** the student solves the exercise.
#
# It checks only the following:
#   1. The directory /home/user/incident_logs exists.
#   2. The three required source log files exist as regular files.
#   3. The byte-for-byte contents of those files exactly match the specification
#      given in the task description.
#
# NOTE:
# * We deliberately do NOT look for the output artefacts
#   (critical_2024-06-12.log, summary.csv) because they do not exist yet and
#   should be created by the student’s solution.
# * The test messages are written to be explicit so that any mismatch will be
#   easy to diagnose.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user").expanduser()
LOG_DIR = HOME / "incident_logs"

# --------------------------------------------------------------------------- #
# Expected contents (including trailing newline on the last line of each file)
# --------------------------------------------------------------------------- #

EXPECTED_APP1 = (
    "2024-06-12 08:55:23,123 - INFO - Service started\n"
    "2024-06-12 09:01:02,456 - ERROR - Failed to connect to database\n"
    "2024-06-12 09:05:10,890 - WARN - Retrying connection\n"
    "2024-06-12 13:15:45,321 - CRITICAL - Out of memory\n"
    "2024-06-13 10:01:57,777 - ERROR - Timeout while processing request\n"
)

EXPECTED_APP2 = (
    "[2024-06-11 23:59:59] DEBUG Initializing\n"
    "[2024-06-12 00:00:01] ERROR Disk full\n"
    "[2024-06-12 08:00:00] INFO Job started\n"
    "[2024-06-12 12:30:00] CRITICAL Kernel panic\n"
    "[2024-06-12 17:45:10] INFO Job finished\n"
    "[2024-06-13 00:01:01] ERROR Disk almost full\n"
)

EXPECTED_SYSTEM = (
    "Jun 12 00:05:01 localhost CRON[1234]: (root) CMD (backup.sh)\n"
    "Jun 12 01:10:45 localhost kernel: [123456.789] ERROR CPU overheating\n"
    "Jun 12 02:22:11 localhost kernel: [123557.890] INFO CPU temperature normalized\n"
    "Jun 13 04:01:33 localhost kernel: [123999.123] CRITICAL Kernel crash\n"
)


@pytest.mark.parametrize(
    "path, expected",
    [
        (LOG_DIR / "app1.log", EXPECTED_APP1),
        (LOG_DIR / "app2.log", EXPECTED_APP2),
        (LOG_DIR / "system.log", EXPECTED_SYSTEM),
    ],
)
def test_log_file_exists_with_exact_content(path: Path, expected: str):
    """
    For each required log file:

    • Verify that the file exists and is a regular file.
    • Verify that its byte-for-byte contents match the specification exactly.

    Any deviation means the initial state is not correct.
    """
    assert LOG_DIR.is_dir(), (
        f"Directory {LOG_DIR} is missing. "
        "The initial fixture must provide /home/user/incident_logs."
    )

    assert path.exists(), f"Expected file {path} does not exist."
    assert path.is_file(), f"Expected {path} to be a regular file."

    # Read the entire file using the same encoding the exercise assumes.
    file_bytes = path.read_bytes()
    expected_bytes = expected.encode()

    assert (
        file_bytes == expected_bytes
    ), (
        f"Contents of {path} do not match the expected initial log. "
        "Ensure the file is unmodified and includes the required trailing newline."
    )