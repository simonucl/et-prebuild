# test_initial_state.py
#
# This pytest suite validates that the initial filesystem state is
# correct *before* the student’s solution runs.  It checks only the
# pre-existing input artefacts and intentionally ignores any output
# artefacts that the student will later create.

import os
import csv
import json
import pytest

MONITORING_DIR = "/home/user/monitoring"
RAW_CSV = os.path.join(MONITORING_DIR, "raw_metrics.csv")
THRESHOLDS_JSON = os.path.join(MONITORING_DIR, "thresholds.json")

EXPECTED_HEADER = [
    "timestamp",
    "hostname",
    "cpu_usage",
    "mem_usage",
    "disk_free",
]

EXPECTED_THRESHOLD_DICT = {
    "cpu_usage": 80,
    "mem_usage": 75,
    "disk_free": 15,
}


def test_monitoring_directory_exists():
    assert os.path.isdir(
        MONITORING_DIR
    ), f"Directory '{MONITORING_DIR}' is missing. It must already exist before the task starts."


def test_raw_metrics_csv_exists_with_correct_header_and_rows():
    assert os.path.isfile(
        RAW_CSV
    ), f"File '{RAW_CSV}' is missing. The task expects the input CSV to be present."

    with open(RAW_CSV, newline="") as fp:
        reader = csv.reader(fp)
        try:
            header = next(reader)
        except StopIteration:
            pytest.fail(f"File '{RAW_CSV}' is empty; expected a header row.")

        assert (
            header == EXPECTED_HEADER
        ), (
            f"Header of '{RAW_CSV}' is incorrect.\n"
            f"Expected: {','.join(EXPECTED_HEADER)}\n"
            f"Found:    {','.join(header)}"
        )

        rows = list(reader)
        expected_row_count = 10  # as provided in the truth value
        assert (
            len(rows) == expected_row_count
        ), f"'{RAW_CSV}' should contain {expected_row_count} data rows; found {len(rows)}."

        # Basic per-row sanity: each row must have exactly 5 columns.
        bad_rows = [
            (idx + 2, row)  # +2 because CSV header is line 1
            for idx, row in enumerate(rows)
            if len(row) != len(EXPECTED_HEADER)
        ]
        if bad_rows:
            msg_lines = [f"Line {ln}: {row} (expected {len(EXPECTED_HEADER)} columns)" for ln, row in bad_rows]
            pytest.fail(
                f"The following rows in '{RAW_CSV}' have an unexpected number of columns:\n" + "\n".join(msg_lines)
            )


def test_thresholds_json_exists_and_is_correct():
    assert os.path.isfile(
        THRESHOLDS_JSON
    ), f"File '{THRESHOLDS_JSON}' is missing. The task expects the JSON thresholds file to be present."

    with open(THRESHOLDS_JSON) as fp:
        try:
            data = json.load(fp)
        except json.JSONDecodeError as exc:
            pytest.fail(f"File '{THRESHOLDS_JSON}' is not valid JSON: {exc}")

    assert (
        data == EXPECTED_THRESHOLD_DICT
    ), (
        f"Contents of '{THRESHOLDS_JSON}' do not match expected thresholds.\n"
        f"Expected: {json.dumps(EXPECTED_THRESHOLD_DICT, indent=2)}\n"
        f"Found:    {json.dumps(data, indent=2)}"
    )