# test_initial_state.py
"""
Pytest suite to validate the *initial* filesystem state **before** the learner
starts working on the ETL exercise.

The checks purposely assert ONLY the prerequisites that must already be in
place, and they confirm the *absence* of anything that the learner is supposed
to create later on.

If any of these tests fail it means the starting environment is wrong, not the
learner’s solution.
"""

import os
from pathlib import Path

import pytest

# --- Constants ----------------------------------------------------------------

HOME = Path("/home/user").expanduser()
RAW_DATA_DIR = HOME / "raw_data"
RAW_FILE = RAW_DATA_DIR / "raw_events_20240315.jsonl"

ETL_ROOT = HOME / "etl"                   # Must NOT exist yet
ETL_RAW_DIR = ETL_ROOT / "raw"
ETL_PROCESSED_DIR = ETL_ROOT / "processed"
ETL_LOGS_DIR = ETL_ROOT / "logs"
CSV_FILE = ETL_PROCESSED_DIR / "events_20240315.csv"
LOG_FILE = ETL_LOGS_DIR / "processing_20240315.log"

EXPECTED_LINES = [
    '{"event_id": 1001, "user_id": 55, "ts": "2024-05-28T12:34:56Z", "meta": "foo"}\n',
    '{"event_id": 1002, "user_id": 56, "ts": "2024-05-28T12:35:56Z", "meta": "bar"}\n',
    '{"event_id": 1003, "user_id": 57, "ts": "2024-05-28T12:36:56Z", "meta": "baz"}\n',
    '{"event_id": 1004, "user_id": 58, "ts": "2024-05-28T12:37:56Z", "meta": "bat"}\n',
]

# ------------------------------------------------------------------------------
# Positive checks: what MUST be present
# ------------------------------------------------------------------------------


def test_raw_data_directory_exists_and_is_dir():
    assert RAW_DATA_DIR.exists(), f"Required directory {RAW_DATA_DIR} is missing."
    assert RAW_DATA_DIR.is_dir(), f"{RAW_DATA_DIR} exists but is not a directory."


def test_raw_events_file_exists_and_is_file():
    assert RAW_FILE.exists(), f"Required file {RAW_FILE} is missing."
    assert RAW_FILE.is_file(), f"{RAW_FILE} exists but is not a regular file."


def test_raw_events_file_content_is_exact_and_newline_terminated():
    content = RAW_FILE.read_bytes()
    # Ensure the file ends with exactly one newline (no extra blank lines)
    assert content.endswith(b"\n"), f"{RAW_FILE} must be newline-terminated."
    lines = content.decode("utf-8").splitlines(keepends=True)
    assert (
        lines == EXPECTED_LINES
    ), (
        f"{RAW_FILE} content is not exactly as expected.\n"
        "Expected lines:\n"
        + "".join(EXPECTED_LINES)
        + "\nFound lines:\n"
        + "".join(lines)
    )

# ------------------------------------------------------------------------------
# Negative checks: what MUST NOT be present yet
# ------------------------------------------------------------------------------


@pytest.mark.parametrize(
    "path_description, path_obj",
    [
        ("ETL root directory", ETL_ROOT),
        ("ETL raw directory", ETL_RAW_DIR),
        ("ETL processed directory", ETL_PROCESSED_DIR),
        ("ETL logs directory", ETL_LOGS_DIR),
        ("Output CSV file", CSV_FILE),
        ("Processing log file", LOG_FILE),
    ],
)
def test_no_etl_artifacts_yet(path_description, path_obj: Path):
    assert not path_obj.exists(), (
        f"{path_description} ({path_obj}) should NOT exist before the student "
        "starts the exercise."
    )