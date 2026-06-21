# test_initial_state.py
#
# This pytest suite validates the *initial* state of the operating system /
# filesystem **before** the student performs any actions for the assignment
# “terse performance summary”.  If any of these tests fail, either the
# environment is mis-configured or the original data has been tampered with.
#
# The tests verify:
#   1. Presence and correctness of /home/user/metrics/raw/dashboard_metrics.csv
#   2. Absence (or pre-existence without artefacts) of output paths that the
#      student is expected to create.
#
# Only Python’s stdlib and pytest are used.

import os
import csv
import stat
from pathlib import Path
from datetime import datetime

RAW_FILE = Path("/home/user/metrics/raw/dashboard_metrics.csv")
SUMMARY_DIR = Path("/home/user/metrics/summary")
SUMMARY_FILE = SUMMARY_DIR / "service_performance_summary.log"
RUN_LOG = Path("/home/user/metrics/run.log")


def test_raw_file_exists_and_is_regular():
    """Verify that the raw metrics file exists and is a regular file."""
    assert RAW_FILE.exists(), f"Required raw file not found at: {RAW_FILE}"
    assert RAW_FILE.is_file(), f"{RAW_FILE} exists but is not a regular file"
    mode = RAW_FILE.stat().st_mode
    assert stat.S_ISREG(mode), f"{RAW_FILE} is not a regular file on disk"


def _parse_raw_rows():
    """Read and return rows (lists) from the raw CSV file."""
    with RAW_FILE.open(newline="", encoding="utf-8") as fh:
        reader = csv.reader(fh)
        rows = list(reader)
    return rows


def test_raw_file_has_exactly_eight_rows():
    """Ensure the raw file has exactly eight non-empty data rows (no header)."""
    rows = _parse_raw_rows()
    assert len(rows) == 8, (
        f"Raw metrics file must contain exactly 8 rows, found {len(rows)}"
    )
    # Ensure no completely blank rows slipped in
    for idx, row in enumerate(rows, start=1):
        assert row, f"Row {idx} is empty in {RAW_FILE}"


def test_raw_file_column_integrity_and_datatypes():
    """Validate each CSV row has 5 columns with correct data types and values."""
    rows = _parse_raw_rows()
    for idx, row in enumerate(rows, start=1):
        assert len(row) == 5, f"Row {idx} should have 5 columns, found {len(row)}"
        ts_str, service, endpoint, latency, success = row

        # Timestamp must be ISO-8601 UTC with trailing 'Z'.
        try:
            datetime.strptime(ts_str, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            assert False, (
                f"Row {idx}: timestamp '{ts_str}' is not ISO-8601 UTC "
                "with trailing 'Z' (e.g., 2023-10-31T01:00:00Z)"
            )

        # Service and endpoint must be non-empty strings.
        assert service.strip(), f"Row {idx}: service name is empty"
        assert endpoint.strip(), f"Row {idx}: endpoint is empty"

        # Latency must be an integer ≥ 0.
        assert latency.isdigit(), f"Row {idx}: latency '{latency}' is not an integer"
        assert int(latency) >= 0, f"Row {idx}: latency {latency} is negative"

        # Success must be either 0 or 1.
        assert success in {"0", "1"}, f"Row {idx}: success '{success}' is not 0 or 1"


def test_raw_file_expected_aggregations():
    """
    Compute aggregations from the raw data and ensure they match the
    authoritative truth values provided in the task description.
    """
    rows = _parse_raw_rows()
    expected = {
        "auth-service": {
            "avg_latency": 141.67,
            "total_requests": 3,
            "total_errors": 1,
        },
        "order-service": {
            "avg_latency": 374.00,
            "total_requests": 5,
            "total_errors": 2,
        },
    }

    # Accumulators
    totals = {}
    for _, service, _, latency, success in rows:
        svc = totals.setdefault(
            service, {"sum_latency": 0, "count": 0, "errors": 0}
        )
        svc["sum_latency"] += int(latency)
        svc["count"] += 1
        if success == "0":
            svc["errors"] += 1

    # Now compare to expected
    assert set(totals) == set(expected), (
        f"Services in raw file {set(totals)} do not match expected {set(expected)}"
    )

    for service, stats in totals.items():
        avg_latency = round(stats["sum_latency"] / stats["count"], 2)
        exp = expected[service]
        assert (
            abs(avg_latency - exp["avg_latency"]) < 1e-9
        ), f"{service}: expected avg latency {exp['avg_latency']}, got {avg_latency}"
        assert (
            stats["count"] == exp["total_requests"]
        ), f"{service}: expected {exp['total_requests']} total requests, got {stats['count']}"
        assert (
            stats["errors"] == exp["total_errors"]
        ), f"{service}: expected {exp['total_errors']} errors, got {stats['errors']}"


def test_summary_directory_state_before_student_action():
    """
    The metrics/summary directory may or may not exist initially.
    If it does exist, it must not yet contain the artefact file
    service_performance_summary.log, because the student has not run
    their solution.
    """
    if SUMMARY_DIR.exists():
        assert SUMMARY_DIR.is_dir(), f"{SUMMARY_DIR} exists but is not a directory"
        assert not SUMMARY_FILE.exists(), (
            f"{SUMMARY_FILE} should NOT exist before the task is executed"
        )
    else:
        # Directory absence is acceptable at this stage.
        assert not SUMMARY_FILE.exists(), (
            f"{SUMMARY_FILE} should NOT exist before the task is executed"
        )


def test_run_log_not_present_yet():
    """run.log must not exist prior to the student executing their solution."""
    assert not RUN_LOG.exists(), (
        f"{RUN_LOG} should not exist before the student runs their commands"
    )