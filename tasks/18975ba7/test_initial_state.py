# test_initial_state.py
#
# This pytest suite validates the *initial* operating-system / filesystem
# state **before** the student begins the task.  It checks that the required
# CSV inventory file exists at the correct absolute path and that its content
# exactly matches the specification provided in the assignment.
#
# NOTE: Per the grading rules we do *not* test for the presence (or absence)
# of any output artefacts that the student is expected to create later.

import os
from pathlib import Path
import pytest

# The absolute path that *must* exist before the exercise starts.
CSV_PATH = Path("/home/user/data/iot_device_inventory.csv")

# The exact expected content of the CSV file (each line must end with <LF>).
EXPECTED_LINES = [
    b"raspberry_pi,edge_node_01\n",
    b"raspberry_pi,edge_node_02\n",
    b"jetson_nano,edge_node_03\n",
    b"esp32,edge_node_04\n",
    b"raspberry_pi,edge_node_05\n",
    b"jetson_nano,edge_node_06\n",
    b"jetson_nano,edge_node_07\n",
    b"beaglebone_black,edge_node_08\n",
    b"esp32,edge_node_09\n",
    b"odroid_c2,edge_node_10\n",
    b"esp32,edge_node_11\n",
    b"beaglebone_black,edge_node_12\n",
    b"odroid_c2,edge_node_13\n",
    b"raspberry_pi,edge_node_14\n",
    b"esp32,edge_node_15\n",
    b"raspberry_pi,edge_node_16\n",
]


def test_csv_file_exists_and_is_regular_file():
    """
    The inventory CSV must exist at the precise path and be a regular file.
    """
    assert CSV_PATH.exists(), (
        f"Required inventory file not found at {CSV_PATH}. "
        "Ensure the file is in place *before* attempting the task."
    )
    assert CSV_PATH.is_file(), (
        f"Expected a regular file at {CSV_PATH}, but found something else "
        "(e.g., directory, symlink). Check the filesystem state."
    )


def test_csv_content_exact_match():
    """
    The CSV content must match the provided truth table exactly—byte for byte.
    We read the file in binary mode so that newline characters are preserved.
    """
    with CSV_PATH.open("rb") as fh:
        data = fh.read()

    # Ensure the file terminates with a single LF (Unix newline).
    assert data.endswith(b"\n"), (
        f"The file {CSV_PATH} must end with a single '\\n' (LF) character."
    )

    # Split into lines (keeping the newline bytes) and validate the count & order.
    actual_lines = data.splitlines(keepends=True)
    assert len(actual_lines) == len(EXPECTED_LINES), (
        f"{CSV_PATH} should contain {len(EXPECTED_LINES)} lines, "
        f"but {len(actual_lines)} were found."
    )

    for idx, (expected, actual) in enumerate(zip(EXPECTED_LINES, actual_lines), start=1):
        assert actual == expected, (
            f"Line {idx} in {CSV_PATH} is incorrect.\n"
            f"Expected: {expected!r}\n"
            f"Found:    {actual!r}"
        )


def test_each_line_has_two_comma_separated_fields():
    """
    Sanity-check: every line should contain exactly two comma-separated fields.
    This guards against malformed CSV input before the student starts parsing.
    """
    with CSV_PATH.open("r", newline="") as fh:
        for idx, line in enumerate(fh, start=1):
            stripped = line.rstrip("\n")
            parts = stripped.split(",")
            assert len(parts) == 2, (
                f"Line {idx} in {CSV_PATH} does not contain exactly two fields "
                f"separated by a single comma: {line!r}"
            )