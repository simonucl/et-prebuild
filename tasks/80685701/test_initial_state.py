# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state that must be in
# place before the student performs any actions.  It purposefully does NOT
# look for (or complain about) the "processed" output directory or any files
# that the student is expected to create later.

import json
from pathlib import Path

PROJECT_ROOT = Path("/home/user/project_data")
EMPLOYEES_CSV = PROJECT_ROOT / "employees.csv"
STATUSES_JSON = PROJECT_ROOT / "statuses.json"


def test_project_data_directory_exists():
    assert PROJECT_ROOT.is_dir(), (
        f"Required directory missing: {PROJECT_ROOT}"
    )


def test_employees_csv_exists_and_contents_are_exact():
    assert EMPLOYEES_CSV.is_file(), (
        f"Required file missing: {EMPLOYEES_CSV}"
    )

    expected_content = (
        "id,name,dept,salary\n"
        "101,Alice Smith,Engineering,90000\n"
        "102,Bob Johnson,Marketing,65000\n"
        "103,Carol Martinez,Engineering,72000\n"
        "104,David Lee,Engineering,68000\n"
        "105,Eve Turner,HR,70000\n"
        "106,Frank Wright,Engineering,80000\n"
    )

    actual_content = EMPLOYEES_CSV.read_text(encoding="utf-8")

    # Compare line-by-line to insulate against an optional trailing newline
    assert actual_content.strip().splitlines() == expected_content.strip().splitlines(), (
        f"File {EMPLOYEES_CSV} does not match the expected contents.\n"
        "---- Expected ----\n"
        f"{expected_content}\n"
        "---- Actual ----\n"
        f"{actual_content}"
    )


def test_statuses_json_exists_and_contents_are_exact():
    assert STATUSES_JSON.is_file(), (
        f"Required file missing: {STATUSES_JSON}"
    )

    expected_json_str = (
        "[\n"
        "  {\"id\": 101, \"active\": true},\n"
        "  {\"id\": 102, \"active\": false},\n"
        "  {\"id\": 103, \"active\": true},\n"
        "  {\"id\": 104, \"active\": false},\n"
        "  {\"id\": 105, \"active\": true},\n"
        "  {\"id\": 106, \"active\": true}\n"
        "]\n"
    )

    actual_content = STATUSES_JSON.read_text(encoding="utf-8")

    # First compare the raw text (ignoring an optional trailing newline),
    # then additionally ensure it's valid JSON to provide clearer feedback
    assert actual_content.strip() == expected_json_str.strip(), (
        f"File {STATUSES_JSON} does not match the expected contents.\n"
        "---- Expected ----\n"
        f"{expected_json_str}\n"
        "---- Actual ----\n"
        f"{actual_content}"
    )

    # Validate JSON parses without error and has 6 items
    try:
        data = json.loads(actual_content)
    except json.JSONDecodeError as e:
        assert False, f"{STATUSES_JSON} is not valid JSON: {e}"

    assert isinstance(data, list) and len(data) == 6, (
        f"{STATUSES_JSON} should be a JSON array with 6 items."
    )