# test_initial_state.py
#
# Pytest suite to validate the **initial** operating-system / filesystem
# state before the student executes any commands for the “curl copy” task.
#
# Rules satisfied:
#   • Uses only stdlib + pytest
#   • Checks the full absolute path
#   • Does NOT look for any output artefacts (/home/user/query_optimization.log)
#   • Provides clear, actionable assertion messages

import pathlib
import pytest

# --------------------------------------------------------------------------- #
# Constants                                                                   
# --------------------------------------------------------------------------- #

MOCK_JSON_PATH = pathlib.Path("/home/user/mock_api_response.json")

EXPECTED_CONTENT = (
    "{\n"
    '  "original_query": "SELECT * FROM employees",\n'
    '  "optimized_query": "SELECT id, name, department FROM employees",\n'
    '  "cost_reduction_percent": 37\n'
    "}\n"
)

# --------------------------------------------------------------------------- #
# Tests                                                                       
# --------------------------------------------------------------------------- #

def test_mock_json_file_exists_and_is_file():
    """
    The mock JSON file that simulates the micro-service response must exist
    as a regular file at the exact absolute path specified by the spec.
    """
    assert MOCK_JSON_PATH.exists(), (
        f"Required file not found: {MOCK_JSON_PATH}. "
        "Ensure the file is present before starting the task."
    )
    assert MOCK_JSON_PATH.is_file(), (
        f"Path exists but is not a regular file: {MOCK_JSON_PATH}."
    )


def test_mock_json_contents_are_exact():
    """
    Ensure the mock JSON file contains the **exact** bytes (including
    new-lines and spaces) expected by the specification.  This guards
    against accidental edits that would break the later byte-for-byte
    comparison performed by the grader.
    """
    content = MOCK_JSON_PATH.read_text(encoding="utf-8")
    assert content == EXPECTED_CONTENT, (
        "The contents of /home/user/mock_api_response.json do not match the "
        "expected template.  They must be exactly:\n\n"
        f"{EXPECTED_CONTENT}\n\n"
        "Actual contents encountered:\n\n"
        f"{content}"
    )