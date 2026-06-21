# test_initial_state.py
#
# Pytest suite that validates the operating-system / filesystem state
# BEFORE the student has performed any actions for the optimisation-solver
# logging task.

import json
from pathlib import Path

API_DIR = Path("/home/user/api_test")
JSON_FILE = API_DIR / "solver_response.json"
LOG_FILE = API_DIR / "optimization_test.log"


def test_api_directory_exists():
    """The /home/user/api_test directory must already be present."""
    assert API_DIR.exists(), f"Required directory {API_DIR} is missing."
    assert API_DIR.is_dir(), f"{API_DIR} exists but is not a directory."


def test_solver_response_json_exists_and_is_file():
    """The solver_response.json must already exist as a regular file."""
    assert JSON_FILE.exists(), (
        f"Required file {JSON_FILE} is missing."
    )
    assert JSON_FILE.is_file(), (
        f"{JSON_FILE} exists but is not a regular file."
    )


def test_solver_response_json_content():
    """
    Validate the exact contents of solver_response.json.

    Expected JSON structure (whitespace and order not important):
        {
          "status": "optimal",
          "x": [1.5, 0.0, 2.5],
          "objective_value": -7.25,
          ... (other keys allowed)
        }
    """
    raw_text = JSON_FILE.read_text(encoding="utf-8")

    # The file should end with a single newline to match the fixture.
    assert raw_text.endswith(
        "\n"
    ), f"{JSON_FILE} should terminate with a newline (\\n)."

    try:
        payload = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise AssertionError(f"{JSON_FILE} does not contain valid JSON: {exc}") from exc

    # Verify mandatory keys are present
    for key in ("status", "objective_value", "x"):
        assert key in payload, f"Key '{key}' is missing from {JSON_FILE}."

    # Verify values
    assert (
        payload["status"] == "optimal"
    ), f"Expected status 'optimal', found '{payload['status']}'."

    assert (
        payload["objective_value"] == -7.25
    ), f"Expected objective_value -7.25, found {payload['objective_value']}."

    expected_x = [1.5, 0.0, 2.5]
    assert (
        payload["x"] == expected_x
    ), f"Expected x {expected_x}, found {payload['x']}."


def test_log_file_not_yet_created():
    """The optimisation log file must NOT exist before the student runs their solution."""
    assert (
        not LOG_FILE.exists()
    ), f"{LOG_FILE} already exists, but it should be created by the student's script."