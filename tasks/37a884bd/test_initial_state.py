# test_initial_state.py
#
# This test-suite verifies that the starting filesystem state is exactly as
# described in the task.  In particular it checks that the service_status.log
# file exists at the expected absolute path and that its contents have not been
# altered.  These guarantees allow the student’s solution (whatever pipeline or
# script they write) to rely on the file’s structure and data.

import pathlib
import pytest

LOG_PATH = pathlib.Path("/home/user/logs/service_status.log")

# The canonical contents of the log file, expressed exactly as they should
# appear on disk (without trailing newline characters).
EXPECTED_LINES = [
    "2023-05-01T00:00:01Z UP 48ms",
    "2023-05-01T00:05:01Z DOWN",
    "2023-05-01T00:10:01Z UP 45ms",
    "2023-05-01T01:15:22Z UP 46ms",
    "2023-05-01T01:20:22Z DOWN",
    "2023-05-01T02:30:31Z UP 47ms",
    "2023-05-01T03:30:31Z UP 44ms",
    "2023-05-01T03:35:31Z DOWN",
    "2023-05-01T04:00:00Z UP 41ms",
    "2023-05-01T04:30:00Z UP 42ms",
]

DOWN_TIMESTAMPS_EXPECTED = [
    "2023-05-01T00:05:01Z",
    "2023-05-01T01:20:22Z",
    "2023-05-01T03:35:31Z",
]


def test_log_file_exists_and_is_file():
    """Ensure the log file exists and is a regular file."""
    assert LOG_PATH.exists(), (
        f"Expected log file at '{LOG_PATH}' is missing. Make sure the file "
        "is present before running the task."
    )
    assert LOG_PATH.is_file(), (
        f"Expected '{LOG_PATH}' to be a regular file, but something else "
        "exists at that path."
    )


def test_log_contents_exact_match():
    """
    Verify that the log file contents are exactly the canonical 10 lines.

    This protects against accidental modification that would invalidate the
    downstream parsing expectations.
    """
    with LOG_PATH.open("r", encoding="utf-8") as f:
        actual_lines = [line.rstrip("\n") for line in f.readlines()]

    assert actual_lines == EXPECTED_LINES, (
        "The contents of the log file do not match the expected canonical "
        "data.\n\n"
        "Expected lines:\n"
        + "\n".join(EXPECTED_LINES)
        + "\n\nActual lines:\n"
        + "\n".join(actual_lines)
    )


def test_down_timestamps_subset_and_order():
    """
    Confirm that the timestamps corresponding to 'DOWN' status lines match the
    oracle list, preserving order and containing no extraneous entries.
    """
    down_ts_found = []
    with LOG_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if line.endswith(" DOWN"):  # safety net, though pattern is fixed
                # The line format for DOWN is:  "<timestamp> DOWN"
                ts, _ = line.split(" ", maxsplit=1)
                down_ts_found.append(ts)

    assert down_ts_found == DOWN_TIMESTAMPS_EXPECTED, (
        "Timestamps extracted from lines with status DOWN do not match the "
        "expected oracle.\n\n"
        f"Expected: {DOWN_TIMESTAMPS_EXPECTED}\n"
        f"Found:    {down_ts_found}"
    )