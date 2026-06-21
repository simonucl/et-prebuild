# test_initial_state.py
#
# Pytest suite that validates the **initial** operating-system state
# before the student’s solution is executed.

import pathlib
import textwrap
import pytest

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------
BASE_DIR = pathlib.Path("/home/user/support/diagnostics")
LOG_FILE = BASE_DIR / "logs.csv"

# Expected byte-exact contents of /home/user/support/diagnostics/logs.csv
EXPECTED_LOGS_CSV = textwrap.dedent("""\
    timestamp,service,status,message
    2023-06-12T10:15:00Z,auth,OK,User login successful
    2023-06-12T10:16:12Z,db,ERROR,Connection timeout
    2023-06-12T10:17:43Z,auth,ERROR,Invalid credentials
    2023-06-12T10:18:07Z,web,OK,Page served
    2023-06-12T10:19:22Z,cache,OK,Cache refreshed
    2023-06-12T10:20:55Z,db,ERROR,Deadlock detected
    2023-06-12T10:21:30Z,web,OK,Page served
    2023-06-12T10:22:18Z,auth,OK,Password reset requested
    """).replace("\n", "\n")  # keep explicit final newline
# Ensure a trailing newline exactly once.
if not EXPECTED_LOGS_CSV.endswith("\n"):
    EXPECTED_LOGS_CSV += "\n"

# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------
def test_directory_structure_exists():
    """
    Validate that the expected directory hierarchy is present.
    """
    assert BASE_DIR.exists(), (
        f"Required directory '{BASE_DIR}' is missing."
        "\nCreate this directory before proceeding."
    )
    assert BASE_DIR.is_dir(), (
        f"'{BASE_DIR}' exists but is not a directory."
        "\nFix the filesystem layout before running the task."
    )


def test_logs_csv_exists():
    """
    Confirm that /home/user/support/diagnostics/logs.csv exists.
    """
    assert LOG_FILE.exists(), (
        f"Required file '{LOG_FILE}' is missing."
        "\nThis CSV must be present before you run your solution."
    )
    assert LOG_FILE.is_file(), (
        f"'{LOG_FILE}' exists but is not a regular file."
        "\nReplace it with a valid file before running the task."
    )


def test_logs_csv_contents_are_exact():
    """
    Check that logs.csv contains exactly the expected data, including the
    final newline.  Any deviation indicates the initial state is wrong.
    """
    actual = LOG_FILE.read_text(encoding="utf-8")
    if actual != EXPECTED_LOGS_CSV:
        # Build a helpful diff-like message without relying on difflib
        expected_lines = EXPECTED_LOGS_CSV.splitlines(keepends=True)
        actual_lines = actual.splitlines(keepends=True)
        diff_head = [
            "Mismatch in contents of logs.csv.\n"
            "Below are the first differing lines (expected vs. actual):"
        ]

        for idx, (exp, act) in enumerate(zip(expected_lines, actual_lines), start=1):
            if exp != act:
                diff_head.append(
                    f"\nLine {idx}:\n"
                    f"    expected: {exp!r}\n"
                    f"      actual: {act!r}"
                )
                break
        else:
            if len(expected_lines) != len(actual_lines):
                diff_head.append(
                    f"\nFile length differs:"
                    f" expected {len(expected_lines)} lines,"
                    f" actual {len(actual_lines)} lines."
                )
            else:
                diff_head.append("\nContents differ but no differing line found.")
        pytest.fail("\n".join(diff_head))