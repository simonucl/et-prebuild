# test_initial_state.py
#
# Pytest suite that verifies the _initial_ operating-system / filesystem
# state expected by the “DB optimisation report” exercise.
#
# The tests purposely avoid checking for any artefacts that the student’s
# solution is supposed to create (e.g. /home/user/db_opt_reports or any
# files inside it).  They focus exclusively on the _input_ CSVs that must
# already be present before the student starts working.
#
# Requirements verified:
#   • /home/user/data/query_stats_2023.csv exists, is readable and contains
#     the exact expected header followed by four data rows with known
#     values.
#   • /home/user/data/query_stats_2024.csv exists, is readable and contains
#     the exact expected header followed by four data rows with known
#     values.
#   • Both files together contain eight data rows in total.
#   • There are no duplicate (query_id, timestamp) pairs across the two
#     files.
#
# Only stdlib + pytest are used.

import csv
from pathlib import Path

import pytest

DATA_DIR = Path("/home/user/data")
CSV_2023 = DATA_DIR / "query_stats_2023.csv"
CSV_2024 = DATA_DIR / "query_stats_2024.csv"

EXPECTED_HEADER = [
    "query_id",
    "db",
    "timestamp",
    "exec_time_ms",
    "cpu_ms",
    "io_reads",
]

EXPECTED_CONTENT_2023 = [
    ["Q1", "db1", "2023-06-15T10:15:30", "120", "80", "200"],
    ["Q2", "db2", "2023-07-20T11:30:00", "250", "150", "300"],
    ["Q3", "db1", "2023-08-05T09:45:10", "90", "60", "100"],
    ["Q4", "db2", "2023-09-12T14:20:05", "310", "200", "400"],
]

EXPECTED_CONTENT_2024 = [
    ["Q1", "db1", "2024-01-18T12:10:20", "110", "70", "190"],
    ["Q5", "db2", "2024-02-25T15:40:00", "340", "220", "450"],
    ["Q6", "db1", "2024-03-03T08:05:55", "95", "65", "110"],
    ["Q7", "db2", "2024-04-10T16:25:30", "280", "180", "350"],
]


def _read_csv(path: Path):
    """Read a CSV file and return (header, rows)."""
    with path.open(newline="") as fp:
        reader = csv.reader(fp)
        header = next(reader)
        rows = list(reader)
    return header, rows


@pytest.mark.parametrize(
    ("csv_path", "expected_rows"),
    [
        (CSV_2023, EXPECTED_CONTENT_2023),
        (CSV_2024, EXPECTED_CONTENT_2024),
    ],
)
def test_csv_exists_and_has_correct_content(csv_path: Path, expected_rows):
    # ---- Existence & readability ------------------------------------------------
    assert csv_path.exists(), f"Required file not found: {csv_path}"
    assert csv_path.is_file(), f"Path exists but is not a file: {csv_path}"
    assert csv_path.stat().st_size > 0, f"File is empty: {csv_path}"

    # ---- Header & row checks ----------------------------------------------------
    header, rows = _read_csv(csv_path)

    assert header == EXPECTED_HEADER, (
        f"{csv_path} has an unexpected header.\n"
        f"Expected: {EXPECTED_HEADER}\n"
        f"Found   : {header}"
    )

    assert len(rows) == 4, (
        f"{csv_path} should contain exactly 4 data rows; "
        f"found {len(rows)} rows instead."
    )

    assert rows == expected_rows, (
        f"{csv_path} contents do not match the expected fixture.\n"
        f"Expected lines:\n{expected_rows}\nGot:\n{rows}"
    )


def test_combined_row_count_and_no_duplicates():
    """Combined files must yield 8 unique data rows."""
    all_rows = []

    for path in (CSV_2023, CSV_2024):
        _, rows = _read_csv(path)
        all_rows.extend(rows)

    assert len(all_rows) == 8, (
        "The two source CSV files together should contain exactly 8 "
        f"data rows, but found {len(all_rows)}."
    )

    seen_keys = set()
    duplicates = []

    for row in all_rows:
        key = (row[0], row[2])  # (query_id, timestamp)
        if key in seen_keys:
            duplicates.append(key)
        seen_keys.add(key)

    assert not duplicates, (
        "Duplicate (query_id, timestamp) pairs were found across the input "
        f"files: {duplicates}"
    )