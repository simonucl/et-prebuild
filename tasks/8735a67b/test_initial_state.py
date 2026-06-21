# test_initial_state.py
"""
Pytest suite that validates the **initial** operating-system / filesystem
state before the student begins the assignment.

Only the _given_ input artefacts are checked; we explicitly stay away from
everything the student is expected to create later on (the entire
/home/user/observability tree).

The test will fail early and verbosely if anything essential is missing or
has been tampered with.
"""

import os
import re
import pytest

# --------------------------------------------------------------------------- #
# CONSTANTS                                                                   #
# --------------------------------------------------------------------------- #

LOG_DIR = "/home/user/logs"
FILE_A = "/home/user/logs/log_serverA.log"
FILE_B = "/home/user/logs/log_serverB.log"

EXPECTED_A_LINES = [
    "2023-10-23T08:00:00Z serverA /api/auth 200 120",
    "2023-10-23T08:00:01Z serverA /api/items 500 34",
    "2023-10-23T08:00:02Z serverA /api/items 200 56",
    "2023-10-23T08:00:03Z serverA /api/cart 502 89",
    "2023-10-23T08:00:04Z serverA /api/cart 200 90",
    "2023-10-23T08:00:05Z serverA /api/cart 200 95",
    "2023-10-23T08:00:06Z serverA /api/auth 503 45",
    "2023-10-23T08:00:07Z serverA /api/auth 200 110",
    "2023-10-23T08:00:08Z serverA /api/items 200 60",
    "2023-10-23T08:00:09Z serverA /api/items 504 40",
]

EXPECTED_B_LINES = [
    "2023-10-23T08:00:00Z serverB /api/auth 200 100",
    "2023-10-23T08:00:01Z serverB /api/items 200 70",
    "2023-10-23T08:00:02Z serverB /api/items 500 30",
    "2023-10-23T08:00:03Z serverB /api/cart 200 85",
    "2023-10-23T08:00:04Z serverB /api/cart 504 90",
    "2023-10-23T08:00:05Z serverB /api/cart 200 80",
    "2023-10-23T08:00:06Z serverB /api/auth 502 55",
    "2023-10-23T08:00:07Z serverB /api/auth 200 95",
    "2023-10-23T08:00:08Z serverB /api/items 200 65",
    "2023-10-23T08:00:09Z serverB /api/items 200 68",
]

ISO_8601_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$"
)

# --------------------------------------------------------------------------- #
# HELPERS                                                                     #
# --------------------------------------------------------------------------- #


def read_lines(path):
    """Return file lines without trailing newline characters."""
    with open(path, encoding="utf-8") as fh:
        return [ln.rstrip("\n") for ln in fh.readlines()]


# --------------------------------------------------------------------------- #
# TESTS                                                                       #
# --------------------------------------------------------------------------- #


def test_log_directory_exists():
    assert os.path.isdir(
        LOG_DIR
    ), f"Required directory {LOG_DIR!r} is missing."


@pytest.mark.parametrize(
    "path,expected",
    [
        (FILE_A, EXPECTED_A_LINES),
        (FILE_B, EXPECTED_B_LINES),
    ],
)
def test_log_file_exists_and_content(path, expected):
    # Existence
    assert os.path.isfile(
        path
    ), f"Required log file {path!r} is missing."

    # Content
    actual = read_lines(path)
    assert (
        actual == expected
    ), f"The contents of {path!r} do not match the expected initial state."


@pytest.mark.parametrize(
    "path",
    [FILE_A, FILE_B],
)
def test_each_line_has_five_fields_and_valid_timestamp(path):
    lines = read_lines(path)
    assert lines, f"{path!r} appears to be empty."

    for idx, line in enumerate(lines, 1):
        parts = line.split(" ")
        assert (
            len(parts) == 5
        ), f"Line {idx} in {path!r} should have exactly 5 space-separated fields, got {len(parts)}: {line!r}"

        ts, hostname, endpoint, status, latency = parts

        # Validate timestamp format (very strict ISO-8601 Zulu)
        assert ISO_8601_RE.match(
            ts
        ), f"Line {idx} in {path!r} has an invalid ISO-8601 timestamp: {ts!r}"

        # Basic sanity checks on the other fields
        assert hostname, f"Line {idx} in {path!r}: hostname field is empty."
        assert endpoint.startswith(
            "/"
        ), f"Line {idx} in {path!r}: endpoint should start with '/', got {endpoint!r}"
        assert status.isdigit() and 100 <= int(status) <= 599, (
            f"Line {idx} in {path!r}: status code should be numeric between 100 and 599, got {status!r}"
        )
        assert latency.isdigit() and int(latency) >= 0, (
            f"Line {idx} in {path!r}: latency should be a non-negative integer, got {latency!r}"
        )