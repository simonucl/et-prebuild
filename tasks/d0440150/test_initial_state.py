# test_initial_state.py
#
# This pytest suite validates the *initial* operating-system / file-system
# state before the learner performs any actions for the “IoT gateway
# CRITICAL-event extraction” task.
#
# It intentionally checks *only* the prerequisites described in the
# specification—no deliverables created by the learner are inspected here.

import os
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# Constants reflecting the expected initial state
# --------------------------------------------------------------------------- #

HOME = Path("/home/user")
LOG_DIR = HOME / "iot_gateway" / "logs"
LOG_FILE = LOG_DIR / "device_events.log"

EXPECTED_LINES = [
    "2023-09-14T22:59:59Z [device-002] CRITICAL: Error code 0x0ABC: Unexpected shutdown\n",
    "2023-09-15T00:00:01Z [device-004] INFO: Boot sequence initiated\n",
    "2023-09-15T08:23:01Z [device-001] INFO: Temperature reading 22.5C\n",
    "2023-09-15T10:00:00Z [device-003] WARNING: Battery low\n",
    "2023-09-15T12:45:33Z [device-007] CRITICAL: Error code 0x0F4A: Sensor failure\n",
    "2023-09-15T13:00:00Z [device-001] CRITICAL: Error code 0x00FF: Overheating detected\n",
    "2023-09-15T15:15:15Z [device-001] CRITICAL: Error code 0x0100: Temperature threshold exceeded\n",
    "2023-09-15T23:59:59Z [device-009] CRITICAL: Error code 0x0011: Network failure\n",
    "2023-09-16T00:00:00Z [device-010] INFO: Boot sequence initiated\n",
]

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #


def _read_lines(path: Path):
    """Read a text file and return the list produced by .readlines()."""
    with path.open("r", encoding="utf-8") as fh:
        return fh.readlines()


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #


def test_log_directory_exists_and_is_directory():
    assert LOG_DIR.exists(), (
        f"Required directory missing: {LOG_DIR}. "
        "Create it (and its parents) before running your solution."
    )
    assert LOG_DIR.is_dir(), f"Expected {LOG_DIR} to be a directory, but it is not."


def test_log_file_exists_and_is_file():
    assert LOG_FILE.exists(), (
        f"Required log file missing: {LOG_FILE}. "
        "Ensure the provided environment contains the raw log."
    )
    assert LOG_FILE.is_file(), f"Expected {LOG_FILE} to be a regular file."


def test_log_file_contents_are_exactly_as_expected():
    # Read the file
    actual_lines = _read_lines(LOG_FILE)

    # 1. Check for the correct number of lines
    expected_line_count = len(EXPECTED_LINES)
    assert (
        len(actual_lines) == expected_line_count
    ), f"{LOG_FILE} should contain exactly {expected_line_count} lines, found {len(actual_lines)}."

    # 2. Check that each line matches exactly (order and newline included)
    mismatches = [
        (idx + 1, exp.rstrip("\n"), act.rstrip("\n"))
        for idx, (exp, act) in enumerate(zip(EXPECTED_LINES, actual_lines))
        if exp != act
    ]

    assert not mismatches, (
        f"{LOG_FILE} contents differ from the expected initial state:\n"
        + "\n".join(
            f"  Line {ln}: expected: {exp!r} | found: {act!r}"
            for ln, exp, act in mismatches
        )
    )

    # 3. Verify that no extra trailing blank lines exist
    if actual_lines and actual_lines[-1] == "\n":
        pytest.fail(
            f"{LOG_FILE} ends with an unexpected blank line. "
            "The last log line should be the 'Boot sequence initiated' entry for device-010."
        )