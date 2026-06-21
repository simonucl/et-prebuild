# test_initial_state.py
#
# This test-suite validates the *initial* state of the workstation
# before the student performs any action.  It confirms that the two
# input log files are present at the expected absolute paths and that
# their contents (including the exact number of ERROR lines) match the
# specification provided in the task description.
#
# NOTE:
# • We deliberately do **NOT** test for `/home/user/error_summary.txt`
#   because that file is expected to be created by the student.
# • Only the Python standard library and `pytest` are used.

import pathlib
import pytest

HOME = pathlib.Path("/home/user")
LOG_A = HOME / "serverA.log"
LOG_B = HOME / "serverB.log"

# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------


def _read_lines(path: pathlib.Path):
    """
    Read a text file and return a list of its lines *without* the trailing
    newline character.  The function raises an informative error if the file
    cannot be read.
    """
    try:
        # Universal newline mode; strip only trailing '\n' for comparison.
        return [line.rstrip("\n") for line in path.read_text(encoding="utf-8").splitlines()]
    except Exception as exc:  # pragma: no cover
        raise AssertionError(f"Could not read expected log file: {path}\n{exc}")


def _assert_file_exists(path: pathlib.Path):
    """Assert that `path` exists and is a regular file."""
    assert path.exists(), f"Expected file does not exist: {path}"
    assert path.is_file(), f"Expected path to be a regular file, but it is not: {path}"


# ----------------------------------------------------------------------
# Expected contents taken verbatim from the problem statement
# ----------------------------------------------------------------------

EXPECTED_SERVERA_LINES = [
    "2023-08-01 12:00:01 INFO Service started",
    "2023-08-01 12:10:15 ERROR Connection timeout",
    "2023-08-01 12:11:00 INFO Reconnected",
    "2023-08-01 12:20:05 ERROR Disk full",
    "2023-08-01 12:30:00 WARNING High memory usage",
]

EXPECTED_SERVERB_LINES = [
    "2023-08-01 12:05:00 INFO Service started",
    "2023-08-01 12:15:45 ERROR Connection refused",
    "2023-08-01 12:16:30 ERROR Connection refused",
    "2023-08-01 12:18:20 INFO Reconnected",
    "2023-08-01 12:25:55 ERROR Disk full",
]

# ----------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------


def test_log_files_exist():
    """Both log files must exist as regular files in /home/user/."""
    _assert_file_exists(LOG_A)
    _assert_file_exists(LOG_B)


@pytest.mark.parametrize(
    "path,expected_lines",
    [
        (LOG_A, EXPECTED_SERVERA_LINES),
        (LOG_B, EXPECTED_SERVERB_LINES),
    ],
)
def test_log_file_contents(path, expected_lines):
    """
    Each log file must contain the exact lines (order + spelling) specified
    in the task description.
    """
    actual_lines = _read_lines(path)
    assert (
        actual_lines == expected_lines
    ), f"Contents of {path} do not match expected lines.\nExpected:\n{expected_lines}\nActual:\n{actual_lines}"


@pytest.mark.parametrize(
    "path,expected_error_count",
    [
        (LOG_A, 2),  # Two ERROR lines in serverA.log
        (LOG_B, 3),  # Three ERROR lines in serverB.log
    ],
)
def test_error_line_counts(path, expected_error_count):
    """Verify that the number of lines containing the string 'ERROR' is as expected."""
    lines = _read_lines(path)
    actual_error_count = sum(1 for line in lines if "ERROR" in line)
    assert (
        actual_error_count == expected_error_count
    ), f"{path.name}: expected {expected_error_count} ERROR lines, found {actual_error_count}"