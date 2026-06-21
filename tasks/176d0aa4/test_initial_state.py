# test_initial_state.py
"""
Pytest suite that validates the initial state of the operating system / filesystem
before the student begins the task.

It checks:
1. The presence of /home/user/logs directory.
2. The presence of /home/user/logs/events.csv file.
3. The exact contents of events.csv (header + 8 rows).
4. Basic integrity of the CSV schema and expected severity counts.

No assertions are made about any artefacts that should be created by the
student’s solution (e.g., event_analysis.db, severity_summary.log).
"""

import os
import csv
import collections
import pytest

LOGS_DIR = "/home/user/logs"
EVENTS_CSV = os.path.join(LOGS_DIR, "events.csv")

EXPECTED_CSV_LINES = [
    "timestamp,severity,message",
    "2023-07-10 10:00:00,INFO,Service started",
    "2023-07-10 10:05:00,WARNING,High memory usage",
    "2023-07-10 10:10:00,ERROR,Service crashed",
    "2023-07-10 10:15:00,INFO,Service restarted",
    "2023-07-10 10:20:00,ERROR,Missing config file",
    "2023-07-10 10:25:00,WARNING,Disk near capacity",
    "2023-07-10 10:30:00,INFO,Health check ok",
    "2023-07-10 10:35:00,ERROR,Service crashed",
]

EXPECTED_SEVERITY_COUNTS = {"ERROR": 3, "INFO": 3, "WARNING": 2}


def test_logs_directory_exists():
    """The /home/user/logs directory must exist."""
    assert os.path.isdir(LOGS_DIR), (
        f"Required directory {LOGS_DIR} is missing. "
        "Create it before proceeding with the task."
    )


def test_events_csv_exists_and_exact_content():
    """
    Verify that events.csv exists and its contents exactly match
    the expected 9 lines (header + 8 data rows).
    """
    assert os.path.isfile(EVENTS_CSV), (
        f"Required CSV file {EVENTS_CSV} is missing."
    )

    with open(EVENTS_CSV, encoding="utf-8") as fh:
        actual_lines = fh.read().splitlines()

    assert actual_lines == EXPECTED_CSV_LINES, (
        "events.csv contents do not match the expected data.\n\n"
        "Expected:\n"
        + "\n".join(EXPECTED_CSV_LINES)
        + "\n\nFound:\n"
        + "\n".join(actual_lines)
    )


def test_events_csv_schema_and_severity_counts():
    """
    Parse events.csv to confirm:
      • It has exactly the three required columns.
      • It contains 8 data rows.
      • The severity distribution matches the specification.
    """
    with open(EVENTS_CSV, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        assert reader.fieldnames == ["timestamp", "severity", "message"], (
            f"CSV header should be ['timestamp', 'severity', 'message'] "
            f"but found {reader.fieldnames}"
        )

        rows = list(reader)

    assert len(rows) == 8, (
        f"events.csv should contain 8 data rows but contains {len(rows)}."
    )

    counts = collections.Counter(row["severity"] for row in rows)
    assert counts == EXPECTED_SEVERITY_COUNTS, (
        f"Severity distribution mismatch.\nExpected: {EXPECTED_SEVERITY_COUNTS}\nFound: {dict(counts)}"
    )