# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the operating system
# before the student’s solution runs.  It deliberately checks only for the
# presence and correctness of the provided input artefacts and **does NOT**
# look for any output directories or files that the student is expected to
# create later.
#
# Requirements verified here:
#   • /home/user/capacity_planner/input/usage_samples.csv must exist
#   • File permissions must be exactly 0644
#   • File must contain exactly five lines (each terminated by '\n')
#   • File content must match the reference sample given in the task text
#
# No third-party packages are used; only Python’s stdlib and pytest.

import os
import stat
from pathlib import Path

import pytest

# Absolute path to the input CSV file
CSV_PATH = Path("/home/user/capacity_planner/input/usage_samples.csv")

# Expected file content (each line must end with a UNIX newline)
EXPECTED_LINES = [
    "timestamp,cpu_percent,mem_used_mb,disk_used_gb,net_in_kbps,net_out_kbps\n",
    "2023-01-01 00:00,45.6,2300,120,300,250\n",
    "2023-01-01 01:00,55.2,2400,121,350,270\n",
    "2023-01-01 02:00,65.4,2500,123,400,310\n",
    "2023-01-01 03:00,35.8,2200,119,280,200\n",
]


@pytest.fixture(scope="module")
def csv_lines():
    """
    Read and return all lines from the CSV file as a list.

    The fixture fails early with a clear message if the file cannot be read.
    """
    if not CSV_PATH.exists():
        pytest.fail(
            f"Required file not found: {CSV_PATH!s}\n"
            "Make sure the sample telemetry data is present before running the task."
        )
    if not CSV_PATH.is_file():
        pytest.fail(f"Expected a regular file at {CSV_PATH!s}, found something else.")

    try:
        lines = CSV_PATH.read_text(encoding="utf-8").splitlines(keepends=True)
    except UnicodeDecodeError as exc:
        pytest.fail(
            f"Failed to read {CSV_PATH!s} as UTF-8 text: {exc}\n"
            "Ensure the file is valid UTF-8 as specified."
        )

    return lines


def test_csv_file_exists():
    """Verify that the CSV file exists and is a regular file."""
    assert CSV_PATH.exists(), f"Missing required file: {CSV_PATH!s}"
    assert CSV_PATH.is_file(), f"Expected {CSV_PATH!s} to be a regular file."


def test_csv_file_permissions():
    """The CSV file must have permissions exactly 0644."""
    mode = stat.S_IMODE(os.stat(CSV_PATH).st_mode)
    expected_mode = 0o644
    assert (
        mode == expected_mode
    ), f"{CSV_PATH!s} has permissions {oct(mode)}, expected {oct(expected_mode)}."


def test_csv_line_count(csv_lines):
    """The CSV file must contain exactly five lines (including header)."""
    assert len(csv_lines) == 5, (
        f"{CSV_PATH!s} is expected to have exactly 5 lines (including header) "
        f"but it has {len(csv_lines)}."
    )


def test_csv_content_exact(csv_lines):
    """
    The CSV file’s content must match the reference sample byte-for-byte,
    including newline characters.
    """
    assert csv_lines == EXPECTED_LINES, (
        f"Content of {CSV_PATH!s} does not match the expected reference.\n\n"
        "Expected lines:\n"
        + "".join(EXPECTED_LINES)
        + "\nActual lines:\n"
        + "".join(csv_lines)
    )