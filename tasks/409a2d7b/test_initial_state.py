# test_initial_state.py
#
# This pytest suite verifies that the *initial* filesystem state is exactly
# what the assignment expects *before* the student begins working.
#
# What we check (and ONLY what we check):
#   • /home/user/data exists and is a directory.
#   • /home/user/data/employees.csv exists and contains the exact expected
#     contents (ignoring a final trailing newline, which may or may not be
#     present).
#   • /home/user/data/salaries.csv exists and contains the exact expected
#     contents (same newline leniency).
#
# We deliberately DO NOT make any assertions about /home/user/output or any
# files that the student will create, per the instructions.

import pathlib
import pytest


HOME = pathlib.Path("/home/user")
DATA_DIR = HOME / "data"

EMPLOYEES_CSV = DATA_DIR / "employees.csv"
SALARIES_CSV = DATA_DIR / "salaries.csv"


EXPECTED_EMPLOYEES = """\
EmployeeID,FirstName,LastName,Department
101,John,Smith,Engineering
102,Alice,Johnson,Marketing
103,Bob,Brown,Sales
104,Carol,Davis,HR
"""

EXPECTED_SALARIES = """\
EmployeeID,BaseSalary,Bonus
101,75000,5000
102,68000,4500
103,72000,4800
104,65000,4200
"""


@pytest.mark.parametrize(
    "path_obj, description",
    [
        (DATA_DIR, "directory /home/user/data"),
        (EMPLOYEES_CSV, "file /home/user/data/employees.csv"),
        (SALARIES_CSV, "file /home/user/data/salaries.csv"),
    ],
)
def test_paths_exist(path_obj: pathlib.Path, description: str):
    """Ensure that the key paths we rely on are present."""
    assert path_obj.exists(), f"Expected {description} to exist, but it is missing."
    if description.startswith("directory"):
        assert path_obj.is_dir(), f"Expected {description} to be a directory."
    else:
        assert path_obj.is_file(), f"Expected {description} to be a regular file."


@pytest.mark.parametrize(
    "csv_path, expected_text, name",
    [
        (EMPLOYEES_CSV, EXPECTED_EMPLOYEES, "employees.csv"),
        (SALARIES_CSV, EXPECTED_SALARIES, "salaries.csv"),
    ],
)
def test_csv_contents_exact(csv_path: pathlib.Path, expected_text: str, name: str):
    """
    Verify that the CSV files contain EXACTLY the expected data.

    We ignore a single trailing newline difference because different editors
    may or may not place it.  All other bytes must match.
    """
    # Read file using universal newlines to normalise line endings.
    file_text = csv_path.read_text(encoding="utf-8")
    # Strip just one trailing newline for leniency.
    assert file_text.rstrip("\n") == expected_text.rstrip(
        "\n"
    ), f"Contents of {csv_path} do not match the expected initial data."