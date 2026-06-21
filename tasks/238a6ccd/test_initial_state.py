# test_initial_state.py
#
# Pytest suite that validates the OS / filesystem *before* the student
# runs any solution code for the “duplicate user_id” task.
#
# The tests confirm that:
#   1. The two shard CSV files exist in the expected absolute locations.
#   2. Both files start with the identical header:  'user_id,timestamp,value'.
#   3. The exact, full contents of each CSV (after the header) match the
#      dataset described in the task statement.
#   4. The logical duplicates implied by those contents are precisely the
#      user-ids {101, 104, 105}.
#
# NOTE:  Per the grading rules we deliberately do *not* test for the presence
#        or absence of any output directories/files (e.g. /home/user/output/*).

import csv
import os
import pytest
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants describing the expected initial state
# ---------------------------------------------------------------------------

DATA_DIR = Path("/home/user/data")
SHARD_A = DATA_DIR / "shard_a.csv"
SHARD_B = DATA_DIR / "shard_b.csv"

EXPECTED_HEADER = ["user_id", "timestamp", "value"]

EXPECTED_A_ROWS = [
    (101, "2023-01-01", "0.5"),
    (102, "2023-01-02", "0.6"),
    (103, "2023-01-03", "0.7"),
    (104, "2023-01-04", "0.8"),
    (105, "2023-01-05", "0.9"),
    (106, "2023-01-06", "1.0"),
    (107, "2023-01-07", "1.1"),
]

EXPECTED_B_ROWS = [
    (104, "2023-01-04", "0.8"),
    (105, "2023-01-05", "0.9"),
    (108, "2023-01-08", "1.2"),
    (109, "2023-01-09", "1.3"),
    (110, "2023-01-10", "1.4"),
    (101, "2023-01-11", "0.55"),
    (111, "2023-01-12", "1.5"),
]

EXPECTED_DUPLICATES = {101, 104, 105}


# ---------------------------------------------------------------------------
# Helper function
# ---------------------------------------------------------------------------

def read_csv_rows(path: Path):
    """
    Read the CSV at `path` and return (header, rows) where:

        header -> list[str]
        rows   -> list[tuple[int, str, str]]

    The `user_id` column is coerced to int for easier set comparison.
    """
    with path.open(newline="") as f:
        rdr = csv.reader(f)
        try:
            header = next(rdr)
        except StopIteration:
            raise AssertionError(f"File {path} is empty.")
        rows = []
        for line_num, row in enumerate(rdr, start=2):  # 1-based lines; header is line 1
            if len(row) != 3:
                raise AssertionError(
                    f"Row {line_num} in {path} has {len(row)} columns, expected 3: {row}"
                )
            try:
                user_id = int(row[0])
            except ValueError:
                raise AssertionError(f"Row {line_num} in {path} has non-integer user_id: {row[0]!r}")
            rows.append((user_id, row[1], row[2]))
    return header, rows


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_files_exist():
    """Both shard CSV files must exist at the exact paths specified."""
    missing = [p for p in (SHARD_A, SHARD_B) if not p.is_file()]
    assert not missing, (
        "Expected CSV file(s) missing:\n" + "\n".join(str(p) for p in missing)
    )


@pytest.mark.parametrize(
    "path, expected_rows",
    [
        (SHARD_A, EXPECTED_A_ROWS),
        (SHARD_B, EXPECTED_B_ROWS),
    ],
)
def test_csv_contents(path, expected_rows):
    """Validate header and row content for each shard."""
    header, rows = read_csv_rows(path)

    # 1. Header must match exactly (order & spelling).
    assert header == EXPECTED_HEADER, (
        f"{path}: header mismatch.\n"
        f"  Expected: {EXPECTED_HEADER}\n"
        f"  Found   : {header}"
    )

    # 2. Row count must match.
    assert len(rows) == len(expected_rows), (
        f"{path}: expected {len(expected_rows)} data rows, found {len(rows)}."
    )

    # 3. Row-by-row comparison (order matters because that is what the task states).
    for idx, (found, exp) in enumerate(zip(rows, expected_rows), start=1):
        assert found == exp, (
            f"{path}: row {idx} mismatch.\n"
            f"  Expected: {exp}\n"
            f"  Found   : {found}"
        )


def test_duplicate_user_ids():
    """Ensure the logical intersection of user_ids across the shards is as described."""
    _, rows_a = read_csv_rows(SHARD_A)
    _, rows_b = read_csv_rows(SHARD_B)

    ids_a = {uid for uid, _, _ in rows_a}
    ids_b = {uid for uid, _, _ in rows_b}
    intersection = ids_a & ids_b

    assert intersection == EXPECTED_DUPLICATES, (
        "Duplicate user_id set mismatch.\n"
        f"  Expected: {sorted(EXPECTED_DUPLICATES)}\n"
        f"  Found   : {sorted(intersection)}"
    )