# test_initial_state.py
#
# This pytest suite validates the initial VM state **before** the student
# performs any action for the “error-code frequency table” task.
#
# Rules enforced:
#   • Only stdlib + pytest are used.
#   • We verify *input* artefacts only, never the expected output paths.
#   • Any failure message pinpoints exactly what is missing or incorrect.

import os
import pytest

LOG_FILE = "/home/user/logs/incident.log"

# The exact 10 log lines expected to be present before the student runs any code.
EXPECTED_LOG_LINES = [
    "[2023-05-10 10:00:00] OK System started.\n",
    "[2023-05-10 10:01:02] ERR42 Disk failure.\n",
    "[2023-05-10 10:02:05] WARN27 High memory usage.\n",
    "[2023-05-10 10:03:07] ERR42 Disk failure.\n",
    "[2023-05-10 10:04:10] ERR99 Network unreachable.\n",
    "[2023-05-10 10:05:12] ERR42 Disk failure.\n",
    "[2023-05-10 10:06:15] WARN27 High memory usage.\n",
    "[2023-05-10 10:07:17] ERR99 Network unreachable.\n",
    "[2023-05-10 10:08:20] INFO11 User login.\n",
    "[2023-05-10 10:09:22] ERR42 Disk failure.\n",
]


def test_log_file_exists_and_is_file():
    """Ensure the incident log file exists and is a regular file."""
    assert os.path.exists(
        LOG_FILE
    ), f"Required log file missing: {LOG_FILE!r}"
    assert os.path.isfile(
        LOG_FILE
    ), f"Expected a regular file at {LOG_FILE!r}, but found something else."


def test_log_file_contents_match_expected():
    """
    Verify that /home/user/logs/incident.log contains exactly the 10
    predefined lines (including trailing newline characters).
    """
    with open(LOG_FILE, "r", encoding="utf-8") as fh:
        actual_lines = fh.readlines()

    # Basic sanity check on line count.
    assert len(actual_lines) == len(
        EXPECTED_LOG_LINES
    ), (
        f"{LOG_FILE!r} should have {len(EXPECTED_LOG_LINES)} lines, "
        f"but it has {len(actual_lines)}."
    )

    # Compare line-by-line for full fidelity.
    mismatches = [
        (idx + 1, exp, act)
        for idx, (exp, act) in enumerate(zip(EXPECTED_LOG_LINES, actual_lines))
        if exp != act
    ]

    assert not mismatches, _format_mismatch_message(mismatches)


def _format_mismatch_message(mismatches):
    """
    Create a detailed error message listing all mismatching lines.

    Each entry is presented as:
        Line <n>: expected '<expected>' but found '<actual>'
    """
    header = "Contents of /home/user/logs/incident.log do not match expectations:"
    lines = [
        f"Line {ln}: expected {exp!r} but found {act!r}"
        for ln, exp, act in mismatches
    ]
    return "\n".join([header] + lines)