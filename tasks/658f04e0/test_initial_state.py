# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the operating‐system
# file-tree before the student’s automation script runs.
#
# Rules respected:
#   • Uses only stdlib + pytest.
#   • Does NOT look for any “output” artefacts (/home/user/data/processed,
#     manifest file, shell script, etc.).
#   • Performs full-path checks and gives helpful failure messages.

from pathlib import Path
import pytest

RAW_BASE = Path("/home/user/data/raw")

# ----------------------------------------------------------------------
# Helper data describing the files that MUST exist before the student starts
# ----------------------------------------------------------------------

EXPECTED_FILES = {
    RAW_BASE / "dataset_A" / "sample1.csv": [
        "gene_id,value",
        "A1,5",
        "A2,7",
    ],
    RAW_BASE / "dataset_A" / "sample2.csv": [
        "gene_id,value",
        "A3,2",
        "A4,9",
    ],
    RAW_BASE / "dataset_B" / "sample1.csv": [
        "gene_id,value",
        "B1,4",
        "B2,1",
    ],
    RAW_BASE / "dataset_B" / "sample2.csv": [
        "gene_id,value",
        "B3,6",
        "B4,3",
    ],
}


# ----------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------

def test_expected_directory_structure_exists():
    """
    The two raw dataset directories and the four expected CSV files must exist.
    No additional *.csv files should be present under /home/user/data/raw/.
    """
    # 1. Check that dataset_A and dataset_B directories exist
    for subdir in ("dataset_A", "dataset_B"):
        p = RAW_BASE / subdir
        assert p.is_dir(), f"Missing directory: {p}"

    # 2. Check that every expected CSV file exists and is a regular file
    for path in EXPECTED_FILES:
        assert path.is_file(), f"Missing raw CSV file: {path}"

    # 3. Ensure there are *exactly* these four CSVs—nothing more, nothing less
    discovered = {p for p in RAW_BASE.rglob("*.csv")}
    assert discovered == set(EXPECTED_FILES.keys()), (
        "Unexpected set of CSV files under /home/user/data/raw/.\n"
        f"Expected: {[str(p) for p in EXPECTED_FILES.keys()]}\n"
        f"Found:    {[str(p) for p in discovered]}"
    )


@pytest.mark.parametrize("path,expected_lines", EXPECTED_FILES.items())
def test_raw_file_contents_are_correct(path: Path, expected_lines):
    """
    Confirm that the contents of each raw CSV exactly match the truth value
    provided in the task description (ignoring trailing newlines).
    """
    contents = path.read_text(encoding="utf-8").splitlines()
    assert contents == expected_lines, (
        f"File contents of {path} do not match expected template.\n"
        f"Expected lines:\n{expected_lines}\n"
        f"Actual lines:\n{contents}"
    )