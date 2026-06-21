# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem
# state before the student performs the exercise described in the prompt.
#
# Only the Python standard library and pytest are used.
#
# What is verified:
#   1. Presence of the required directories.
#   2. Presence and exact JSON content of the two seed files
#      /home/user/perfdata/performance.json and
#      /home/user/perfdata/schema.json.
#   3. That /home/user/reports/ exists **and is empty** (as mandated).
#
# The tests purposefully DO NOT look for any of the artefacts that the
# student is expected to create later (slow_requests.json,
# summary.log, etc.).

import json
import os
from pathlib import Path

import pytest

PERFDATA_DIR = Path("/home/user/perfdata")
REPORTS_DIR = Path("/home/user/reports")
PERF_JSON = PERFDATA_DIR / "performance.json"
SCHEMA_JSON = PERFDATA_DIR / "schema.json"


@pytest.mark.parametrize(
    "path",
    [
        PERFDATA_DIR,
        REPORTS_DIR,
    ],
)
def test_required_directories_exist(path):
    assert path.is_dir(), f"Required directory {path} is missing."


def test_reports_directory_is_initially_empty():
    # The reports directory must start out empty; the student will populate it.
    contents = [p for p in REPORTS_DIR.iterdir() if not p.name.startswith(".")]
    assert (
        len(contents) == 0
    ), f"{REPORTS_DIR} is expected to be empty before the task begins, but it contains: {contents}"


@pytest.mark.parametrize(
    "file_path",
    [
        PERF_JSON,
        SCHEMA_JSON,
    ],
)
def test_seed_files_exist(file_path):
    assert file_path.is_file(), f"Required file {file_path} is missing."


def test_performance_json_content():
    with open(PERF_JSON, "r", encoding="utf-8") as fh:
        data = json.load(fh)

    expected = {
        "timestamp": "2023-11-05T14:25:30Z",
        "environment": "staging",
        "runs": [
            {"service": "auth", "response_time_ms": 120},
            {"service": "payment", "response_time_ms": 860},
            {"service": "search", "response_time_ms": 450},
            {"service": "inventory", "response_time_ms": 1020},
            {"service": "auth", "response_time_ms": 200},
            {"service": "payment", "response_time_ms": 780},
            {"service": "search", "response_time_ms": 300},
        ],
    }

    assert (
        data == expected
    ), "performance.json does not match the expected initial content."


def test_schema_json_content():
    with open(SCHEMA_JSON, "r", encoding="utf-8") as fh:
        schema = json.load(fh)

    # Build the exact schema we expect.
    expected_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": ["timestamp", "environment", "runs"],
        "properties": {
            "timestamp": {"type": "string", "format": "date-time"},
            "environment": {"type": "string", "enum": ["dev", "staging", "prod"]},
            "runs": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["service", "response_time_ms"],
                    "properties": {
                        "service": {"type": "string"},
                        "response_time_ms": {"type": "integer", "minimum": 0},
                    },
                    "additionalProperties": False,
                },
            },
        },
        "additionalProperties": False,
    }

    assert (
        schema == expected_schema
    ), "schema.json does not match the expected initial JSON schema."