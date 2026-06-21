# test_initial_state.py
"""
Pytest suite that validates the initial filesystem / data state
before the student executes the assignment script.
Only standard library + pytest are used.

Checked truths:
1. Directory /home/user/data exists.
2. File /home/user/data/metrics.csv exists.
3. File /home/user/data/metrics.csv contains exactly the expected
   header and data rows (nothing more, nothing less).
4. The rows that satisfy the alert condition (cpu > 85 OR memory > 90)
   are exactly the ones spelled out in the task description.
"""

import csv
from pathlib import Path

import pytest

DATA_DIR = Path("/home/user/data")
CSV_PATH = DATA_DIR / "metrics.csv"

# Ground-truth from the problem statement
EXPECTED_LINES = [
    "server,cpu,memory",
    "web-01,65,70",
    "app-02,88,91",
    "db-01,92,80",
    "cache-01,55,40",
    "web-02,83,95",
]

EXPECTED_ALERT_ROWS = [
    ("app-02", 88, 91),
    ("db-01", 92, 80),
    ("web-02", 83, 95),
]


def test_data_directory_exists():
    assert DATA_DIR.is_dir(), (
        f"Required directory '{DATA_DIR}' is missing.\n"
        "Create the directory and place metrics.csv inside it."
    )


def test_metrics_csv_exists():
    assert CSV_PATH.is_file(), (
        f"Required file '{CSV_PATH}' is missing.\n"
        "Ensure the CSV file is present before proceeding."
    )


def test_metrics_csv_exact_contents():
    """Verify that metrics.csv contains exactly the expected lines."""
    with CSV_PATH.open(encoding="utf-8") as fh:
        lines = [line.rstrip("\n") for line in fh]

    assert lines == EXPECTED_LINES, (
        "The contents of metrics.csv do not match the expected truth.\n"
        f"Expected ({len(EXPECTED_LINES)} lines):\n{EXPECTED_LINES}\n\n"
        f"Found ({len(lines)} lines):\n{lines}"
    )


def test_alert_condition_rows_match_truth():
    """Re-evaluate the alert condition and ensure it matches the stated truth."""
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        rows = [
            (row["server"], int(row["cpu"]), int(row["memory"]))
            for row in reader
        ]

    # Recompute which rows should trigger an alert
    computed_alerts = [
        (server, cpu, memory)
        for (server, cpu, memory) in rows
        if cpu > 85 or memory > 90
    ]

    assert computed_alerts == EXPECTED_ALERT_ROWS, (
        "Rows that satisfy the alert condition (cpu>85 OR memory>90) "
        "do not match the expected set.\n"
        f"Expected ({len(EXPECTED_ALERT_ROWS)} rows): {EXPECTED_ALERT_ROWS}\n"
        f"Found    ({len(computed_alerts)} rows): {computed_alerts}"
    )