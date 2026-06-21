# test_initial_state.py
#
# This test-suite verifies that the starting filesystem snapshot is exactly
# what the exercise description promises *before* the student (agent) starts
# working.  It checks
#
# 1.  Presence of the expected directories and files.
# 2.  Absence of any artefacts that must only appear *after* the task
#    (validation.log, processed/summary_20231201.json, …).
# 3.  JSON contents of the three raw log files and the JSON-Schema file.

import json
from pathlib import Path

import pytest

ROOT = Path("/home/user/diagnostics")
RAW_DIR = ROOT / "raw"
SCHEMA_DIR = ROOT / "schema"

LOG1 = RAW_DIR / "log1.json"
LOG2 = RAW_DIR / "log2.json"
LOG3 = RAW_DIR / "log3.json"
SCHEMA_FILE = SCHEMA_DIR / "diagnostic.schema.json"

# Expected JSON contents ------------------------------------------------------

EXPECTED_LOG1 = {
    "service": "auth",
    "status": "running",
    "errors": [],
}

EXPECTED_LOG2 = {
    "service": "payments",
    "status": "degraded",
    "errors": ["timeout connecting to db", "retry failure"],
}

EXPECTED_LOG3 = {
    "status": "running",
    "errors": [],
}

EXPECTED_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["service", "status", "errors"],
    "properties": {
        "service": {"type": "string"},
        "status": {"type": "string"},
        "errors": {
            "type": "array",
            "items": {"type": "string"},
        },
    },
    "additionalProperties": False,
}


# Helper ----------------------------------------------------------------------


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


# Tests -----------------------------------------------------------------------


def test_required_directories_exist():
    for directory in (RAW_DIR, SCHEMA_DIR):
        assert directory.is_dir(), f"Required directory {directory} is missing"


def test_required_files_exist():
    for file_ in (LOG1, LOG2, LOG3, SCHEMA_FILE):
        assert file_.is_file(), f"Required file {file_} is missing"


def test_no_output_files_yet():
    """
    validation.log and the processed/summary must NOT exist prior to running
    the student’s solution.
    """
    validation_log = ROOT / "validation.log"
    processed_dir = ROOT / "processed"
    summary_file = processed_dir / "summary_20231201.json"

    assert not validation_log.exists(), (
        f"Output file {validation_log} should not exist at the initial state"
    )
    # The processed directory itself may or may not exist yet, but if it does,
    # the summary file must not be present.
    if processed_dir.exists():
        assert processed_dir.is_dir(), f"{processed_dir} exists but is not a directory"
        assert not summary_file.exists(), (
            f"Summary file {summary_file} should not exist at the initial state"
        )


@pytest.mark.parametrize(
    "path_,expected",
    [
        (LOG1, EXPECTED_LOG1),
        (LOG2, EXPECTED_LOG2),
        (LOG3, EXPECTED_LOG3),
    ],
)
def test_raw_log_contents(path_: Path, expected: dict):
    data = load_json(path_)
    assert data == expected, f"Content of {path_} does not match the expected fixture"


def test_schema_file_content():
    data = load_json(SCHEMA_FILE)
    assert data == EXPECTED_SCHEMA, (
        f"Content of {SCHEMA_FILE} does not match the expected JSON-Schema"
    )