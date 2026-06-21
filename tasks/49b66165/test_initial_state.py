# test_initial_state.py
#
# This pytest suite validates that the operative system / filesystem
# is in the *initial* state required by the “performance benchmark” task.
#
# It intentionally fails fast and with clear error messages if:
#   • the source dataset is missing or malformed,
#   • there are more (or fewer) than the three expected CSV files,
#   • the analysis_results directory already exists (it must be created
#     by the student, not be present beforehand).

from pathlib import Path
import csv
import pytest

# ---------------------------------------------------------------------------
# CONSTANTS
# ---------------------------------------------------------------------------

HOME_DIR = Path("/home/user")
DATASET_DIR = HOME_DIR / "datasets" / "performance"
EXPECTED_CSV_FILES = {
    "sales_q1.csv",
    "sales_q2.csv",
    "sales_q3.csv",
}
EXPECTED_HEADER = ["OrderID", "Units", "Revenue"]
ANALYSIS_RESULTS_DIR = HOME_DIR / "analysis_results"

# ---------------------------------------------------------------------------
# HELPER UTILITIES
# ---------------------------------------------------------------------------


def _read_csv_rows(path: Path):
    """
    Return the CSV rows (as lists) from *path* while making sure the file
    is RFC-4180 compliant enough for our simple use-case.

    Raises an assertion error with a descriptive message if the file does
    not meet the minimal expectations (header line, at least one data row,
    no blank lines, correct number of columns).
    """
    with path.open(newline="") as fh:
        reader = csv.reader(fh)
        rows = list(reader)

    assert rows, f"{path} is empty."
    assert (
        rows[0] == EXPECTED_HEADER
    ), f"{path} has an unexpected header. Expected {EXPECTED_HEADER!r}, got {rows[0]!r}"

    # Ensure every data row has exactly 3 columns and no blanks
    for idx, row in enumerate(rows[1:], start=2):  # 1-based, include header
        assert (
            len(row) == 3
        ), f"{path}: line {idx} must have exactly 3 comma-separated fields"

        # Basic sanity: OrderID and numeric values are digit-only.
        order_id, units, revenue = row
        assert order_id.isdigit(), f"{path}: line {idx} OrderID must be digits only"
        assert units.isdigit(), f"{path}: line {idx} Units must be digits only"
        assert revenue.isdigit(), f"{path}: line {idx} Revenue must be digits only"

    return rows


# ---------------------------------------------------------------------------
# TESTS
# ---------------------------------------------------------------------------


def test_dataset_directory_exists():
    assert DATASET_DIR.is_dir(), (
        "The dataset directory "
        f"{DATASET_DIR} does not exist. It must be present before you begin."
    )


def test_dataset_contains_exact_three_csv_files():
    files_in_dir = {p.name for p in DATASET_DIR.iterdir() if p.is_file()}
    assert (
        files_in_dir == EXPECTED_CSV_FILES
    ), (
        f"The dataset directory must contain exactly the files "
        f"{sorted(EXPECTED_CSV_FILES)}, but it contains {sorted(files_in_dir)}."
    )


@pytest.mark.parametrize("csv_filename", sorted(EXPECTED_CSV_FILES))
def test_each_csv_file_has_correct_format(csv_filename):
    csv_path = DATASET_DIR / csv_filename
    # Presence already validated; now inspect contents.
    rows = _read_csv_rows(csv_path)

    # The specification says each quarter file contains header + 3 data rows
    expected_line_count = 1 + 3
    assert (
        len(rows) == expected_line_count
    ), f"{csv_path} should have {expected_line_count} lines (1 header + 3 data), found {len(rows)}."


def test_analysis_results_directory_absent():
    """
    /home/user/analysis_results/ must *not* exist at the very start.  It is
    the student's responsibility to create it.  If it is already present,
    the initial state is invalid.
    """
    assert not ANALYSIS_RESULTS_DIR.exists(), (
        f"{ANALYSIS_RESULTS_DIR} already exists, but it must be created by the "
        "student during the task, not be present beforehand."
    )