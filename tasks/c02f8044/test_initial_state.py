# test_initial_state.py
"""
Pytest suite that validates the operating-system state **before** the student
carries out the FinOps archiving task.

It asserts that:
1. /home/user/cloud_reports/ exists and is a directory.
2. That directory contains *exactly* the 12 detailed cost report CSVs,
   one yearly summary CSV, and one README.txt (14 files total).
3. Every detailed CSV has the precise two-line content specified.
4. The yearly summary CSV has the precise single-row content specified.

Nothing is checked about /home/user/backup/ or any other output artefacts,
per the grading rules.
"""
from pathlib import Path

import pytest

CLOUD_REPORTS_DIR = Path("/home/user/cloud_reports")

# Expected file sets -----------------------------------------------------------

# 1. The 12 monthly detailed reports
DETAILED_REPORTS = [
    f"cost_report_2023-{month:02}.csv" for month in range(1, 13)
]

# 2. The yearly summary and README
EXTRA_FILES = ["summary_2023.csv", "README.txt"]

EXPECTED_FILES = sorted(DETAILED_REPORTS + EXTRA_FILES)


# -----------------------------------------------------------------------------


def test_cloud_reports_directory_exists_and_is_dir():
    assert CLOUD_REPORTS_DIR.exists(), (
        f"Directory {CLOUD_REPORTS_DIR} is missing. "
        "It must be present before the task begins."
    )
    assert CLOUD_REPORTS_DIR.is_dir(), (
        f"{CLOUD_REPORTS_DIR} exists but is not a directory."
    )


def test_cloud_reports_contains_exact_expected_files():
    files_found = sorted(p.name for p in CLOUD_REPORTS_DIR.iterdir())
    assert files_found == EXPECTED_FILES, (
        "The directory /home/user/cloud_reports/ should contain exactly the "
        "following 14 files:\n"
        + "\n".join(EXPECTED_FILES)
        + "\nBut instead it contains:\n"
        + "\n".join(files_found)
    )


@pytest.mark.parametrize("csv_name", DETAILED_REPORTS)
def test_each_detailed_csv_has_correct_content(csv_name):
    """
    Verify the two-line content of each cost_report_2023-XX.csv file.
    Expected (note the newline at the end of each line):

        Month,TotalUSD
        2023-XX,1000
    """
    path = CLOUD_REPORTS_DIR / csv_name
    assert path.is_file(), f"Expected file {path} to exist."
    expected_month = csv_name.split("_")[2].split(".")[0]  # '2023-XX'
    expected_content = f"Month,TotalUSD\n{expected_month},1000\n"
    actual_content = path.read_text(encoding="utf-8")
    assert (
        actual_content == expected_content
    ), f"File {csv_name} has incorrect content.\nExpected:\n{expected_content!r}\nGot:\n{actual_content!r}"


def test_summary_csv_has_correct_content():
    """
    Verify the one-row content of summary_2023.csv:

        Year,TotalUSD
        2023,12000
    """
    path = CLOUD_REPORTS_DIR / "summary_2023.csv"
    assert path.is_file(), "summary_2023.csv is missing."
    expected_content = "Year,TotalUSD\n2023,12000\n"
    actual_content = path.read_text(encoding="utf-8")
    assert (
        actual_content == expected_content
    ), "summary_2023.csv has incorrect content."