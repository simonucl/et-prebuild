# test_initial_state.py
#
# This pytest suite validates that the *initial* filesystem state required
# for the assignment is present **before** the student performs any action.
#
# It intentionally checks ONLY the prerequisite artefacts and avoids any
# verification of the files/directories that the student is expected to
# create in their solution.

from pathlib import Path
import pytest

# ---------------------------------------------------------------------------
# Constants describing the expected initial state
# ---------------------------------------------------------------------------

EMPLOYEES_CSV = Path("/home/user/data/employees.csv")

EXPECTED_CSV_CONTENT = (
    "id,name,department,salary\n"
    "1,John Smith,Engineering,90000\n"
    "2,Jane Doe,Marketing,65000\n"
    "3,Bob Johnson,Engineering,80000\n"
    "4,Alice Davis,HR,60000\n"
    "5,Charlie Brown,Engineering,72000\n"
    "6,Eve Black,Engineering,68000\n"
    "7,Frank White,Sales,70000\n"
).encode("utf-8")  # keep Unix newlines and final \n intact


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_employees_csv_exists_and_is_file():
    """
    The input CSV must exist and be a regular file.
    """
    assert EMPLOYEES_CSV.exists(), (
        f"Required input file not found: {EMPLOYEES_CSV}"
    )
    assert EMPLOYEES_CSV.is_file(), (
        f"Expected {EMPLOYEES_CSV} to be a file, but it is not."
    )


def test_employees_csv_contents_exact_match():
    """
    The contents of employees.csv must exactly match the specification,
    including Unix newlines and a trailing newline on the final row.
    """
    actual_bytes = EMPLOYEES_CSV.read_bytes()

    # Helpful diagnostics if the file differs
    if actual_bytes != EXPECTED_CSV_CONTENT:
        # Provide a diff-like hint without relying on external libraries
        actual_lines = actual_bytes.decode("utf-8", errors="replace").splitlines(keepends=True)
        expected_lines = EXPECTED_CSV_CONTENT.decode("utf-8").splitlines(keepends=True)

        max_len = max(len(actual_lines), len(expected_lines))
        mismatch_report = []
        for i in range(max_len):
            exp_line = expected_lines[i].rstrip("\n") if i < len(expected_lines) else "<missing>"
            act_line = actual_lines[i].rstrip("\n") if i < len(actual_lines) else "<missing>"
            if exp_line != act_line:
                mismatch_report.append(f"Line {i+1}: expected '{exp_line}' but found '{act_line}'")

        diff_msg = "\n".join(mismatch_report[:10])  # limit noise
        pytest.fail(
            "employees.csv contents do not match the expected initial data.\n"
            + (diff_msg or "File length differs.")
        )

    # Additional guard: ensure no Windows CRLF sequences
    assert b"\r\n" not in actual_bytes, (
        "employees.csv must use Unix newlines ('\\n'), "
        "but Windows newlines ('\\r\\n') were detected."
    )