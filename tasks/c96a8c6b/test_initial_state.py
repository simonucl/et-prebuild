# test_initial_state.py
# Pytest suite that validates the operating-system / filesystem state
# BEFORE the student performs any action for the “release-manager automation” task.
#
# Rules respected:
#   • Uses only stdlib + pytest
#   • Does NOT test for any of the output artefacts that the student is asked to create
#   • Performs all checks against absolute paths under /home/user
#   • Produces clear, actionable failure messages

import csv
import os
from pathlib import Path

import pytest


RELEASES_DIR = Path("/home/user/releases")
CSV_PATH = RELEASES_DIR / "deployments.csv"

EXPECTED_HEADER = [
    "id",
    "project",
    "version",
    "environment",
    "status",
    "release_date",
]

# Explicitly lay out the expected rows so the test suite can
# confirm file integrity, ordering, counts, etc.
EXPECTED_ROWS = [
    {
        "id": "1",
        "project": "frontend",
        "version": "1.4.2",
        "environment": "staging",
        "status": "completed",
        "release_date": "2024-01-12",
    },
    {
        "id": "2",
        "project": "backend",
        "version": "2.3.0",
        "environment": "production",
        "status": "pending",
        "release_date": "2024-03-05",
    },
    {
        "id": "3",
        "project": "api",
        "version": "3.1.1",
        "environment": "staging",
        "status": "pending",
        "release_date": "2024-03-11",
    },
    {
        "id": "4",
        "project": "billing",
        "version": "4.0.0",
        "environment": "production",
        "status": "aborted",
        "release_date": "2024-02-09",
    },
    {
        "id": "5",
        "project": "frontend",
        "version": "1.4.3",
        "environment": "production",
        "status": "pending",
        "release_date": "2024-03-14",
    },
    {
        "id": "6",
        "project": "worker",
        "version": "0.9.8",
        "environment": "staging",
        "status": "completed",
        "release_date": "2024-02-28",
    },
]


@pytest.fixture(scope="module")
def csv_lines():
    """
    Read the CSV file raw (binary aware) so we can verify newline behaviour
    and guarantee UTF-8 encoding.
    """
    if not CSV_PATH.exists():
        pytest.fail(f"Required CSV file not found at absolute path: {CSV_PATH}")

    # Ensure it's a regular file and not a directory or symlink.
    if not CSV_PATH.is_file():
        pytest.fail(f"Expected a regular file at {CSV_PATH}, found something else.")

    try:
        text = CSV_PATH.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        pytest.fail(f"File {CSV_PATH} is not valid UTF-8: {exc}")

    lines = text.splitlines(keepends=True)  # retain newline characters
    return lines


def test_csv_has_exact_line_count(csv_lines):
    """The CSV must have exactly 7 lines (1 header + 6 data rows)."""
    assert (
        len(csv_lines) == 7
    ), f"{CSV_PATH} should contain 7 lines (1 header + 6 rows); found {len(csv_lines)}."


def test_every_line_ends_with_lf(csv_lines):
    """Every line in the CSV should terminate with a single LF character (\\n)."""
    for idx, raw_line in enumerate(csv_lines, start=1):
        assert raw_line.endswith("\n"), (
            f"Line {idx} in {CSV_PATH} does not end with a single LF character."
        )


@pytest.fixture(scope="module")
def csv_rows():
    """Parse the CSV into a list of dictionaries using the csv.DictReader."""
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    return rows


def test_header_columns_are_correct(csv_rows):
    """Verify that the header columns exist and are in the correct order."""
    actual_header = list(csv_rows[0].keys())
    assert (
        actual_header == EXPECTED_HEADER
    ), f"CSV header mismatch.\nExpected: {EXPECTED_HEADER}\nActual:   {actual_header}"


def test_csv_rows_exact_match(csv_rows):
    """The CSV file's rows must exactly match the expected data set."""
    assert csv_rows == EXPECTED_ROWS, (
        "CSV contents do not match the expected truth set.\n"
        "Differences:\n"
        f"Expected: {EXPECTED_ROWS}\n"
        f"Actual:   {csv_rows}"
    )


def test_status_counts_are_correct(csv_rows):
    """Ensure the status counts (PENDING, COMPLETED, ABORTED) are correct."""
    status_counter = {"pending": 0, "completed": 0, "aborted": 0}
    for row in csv_rows:
        status = row["status"]
        if status not in status_counter:
            pytest.fail(
                f"Unexpected status value '{status}' encountered in {CSV_PATH}."
            )
        status_counter[status] += 1

    expected_counts = {"pending": 3, "completed": 2, "aborted": 1}
    assert (
        status_counter == expected_counts
    ), f"Status counts mismatch.\nExpected: {expected_counts}\nActual:   {status_counter}"


def test_releases_directory_exists():
    """Top-level releases directory must exist and be a directory."""
    assert RELEASES_DIR.exists(), f"Directory {RELEASES_DIR} does not exist."
    assert RELEASES_DIR.is_dir(), f"{RELEASES_DIR} exists but is not a directory."