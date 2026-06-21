# test_initial_state.py
#
# Pytest suite that validates the *initial* filesystem / OS state
# before the student performs any actions for the “FinOps analyst”
# exercise.  These tests assert that:
#
# 1. The mock-API JSON files are present at the exact paths given.
# 2. The JSON content of those files matches the canonical data
#    supplied in the task description.
# 3. No artefact that the student is expected to create later
#    (response files or summary.txt) exists yet.
#
# If any assertion fails, the accompanying message pinpoints what is
# missing or incorrect so the student knows exactly what to fix.
#
# ONLY standard library + pytest are used, as required.

import json
from pathlib import Path

import pytest

# ---------- Constants ---------- #

HOME = Path("/home/user")
MOCK_API_DIR = HOME / "finops" / "mock_api"
RESPONSES_DIR = HOME / "finops" / "responses"

COST_DATA_FILE = MOCK_API_DIR / "cost-data.json"
RIGHTSIZING_FILE = MOCK_API_DIR / "rightsizing-suggestions.json"

EXPECTED_COST_DATA = {
    "accountId": "123456789012",
    "currency": "USD",
    "totalMonthlyCost": 1423.55,
    "services": [
        {"name": "AmazonEC2", "monthlyCost": 823.10},
        {"name": "AmazonS3", "monthlyCost": 211.22},
        {"name": "AmazonRDS", "monthlyCost": 389.23},
    ],
}

EXPECTED_RIGHTSIZING = {
    "generatedAt": "2023-10-01T00:00:00Z",
    "suggestions": [
        {"name": "i-02468ec2", "monthlySavings": 120.35},
        {"name": "i-13579ec2", "monthlySavings": 98.99},
        {"name": "db-42rds", "monthlySavings": 45.10},
    ],
}

# Artefacts that must NOT exist yet (created by the student later)
SHOULD_NOT_EXIST = [
    RESPONSES_DIR / "cost_data_response.json",
    RESPONSES_DIR / "rightsizing_response.json",
    HOME / "finops" / "summary.txt",
]


# ---------- Helper Functions ---------- #


def load_json(path: Path):
    """Load JSON from *path* and return the parsed object."""
    try:
        with path.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    except json.JSONDecodeError as e:  # pragma: no cover
        pytest.fail(f"File {path} exists but contains invalid JSON: {e}")


# ---------- Tests ---------- #


def test_mock_api_directory_exists():
    assert MOCK_API_DIR.is_dir(), (
        f"Expected directory {MOCK_API_DIR} to exist, "
        "but it does not. Ensure the mock API folder is present."
    )


def test_cost_data_json_exists_and_has_expected_content():
    assert COST_DATA_FILE.is_file(), (
        f"Expected file {COST_DATA_FILE} to exist, but it is missing."
    )

    data = load_json(COST_DATA_FILE)
    assert data == EXPECTED_COST_DATA, (
        f"Contents of {COST_DATA_FILE} do not match the expected fixture.\n"
        "If you changed the file, revert it to the original mock data."
    )


def test_rightsizing_json_exists_and_has_expected_content():
    assert RIGHTSIZING_FILE.is_file(), (
        f"Expected file {RIGHTSIZING_FILE} to exist, but it is missing."
    )

    data = load_json(RIGHTSIZING_FILE)
    assert data == EXPECTED_RIGHTSIZING, (
        f"Contents of {RIGHTSIZING_FILE} do not match the expected fixture.\n"
        "If you changed the file, revert it to the original mock data."
    )


def test_no_student_output_files_exist_yet():
    missing = [p for p in SHOULD_NOT_EXIST if p.exists()]
    assert not missing, (
        "The following artefacts already exist but should NOT be present "
        "before the exercise is attempted:\n"
        + "\n".join(str(p) for p in missing)
    )