# test_initial_state.py
"""
Pytest suite that validates the expected initial filesystem state
before the student performs any actions for the “API summary” task.
"""

from pathlib import Path
import json
import pytest

STATUS_PATH = Path("/home/user/mock_responses/status.json")
METRICS_PATH = Path("/home/user/mock_responses/metrics.json")
SCRIPT_PATH = Path("/home/user/scripts/api_summary.sh")
LOG_PATH = Path("/home/user/logs/api_summary.log")


def read_single_line_json(path: Path):
    """
    Helper that reads a file expected to contain a single-line JSON string
    and returns the corresponding dict. Whitespace and a trailing newline
    (if any) are ignored for robust comparison.
    """
    content = path.read_text().strip()
    try:
        return json.loads(content)
    except json.JSONDecodeError as exc:  # pragma: no cover
        pytest.fail(f"{path} does not contain valid JSON: {exc}")


def test_mock_response_files_exist():
    """Both mock response JSON files must exist."""
    assert STATUS_PATH.is_file(), f"Missing file: {STATUS_PATH}"
    assert METRICS_PATH.is_file(), f"Missing file: {METRICS_PATH}"


def test_status_json_content():
    """status.json must contain exactly the expected key/value pairs."""
    data = read_single_line_json(STATUS_PATH)
    expected = {"service": "alpha", "status": "ok"}
    assert data == expected, (
        f"{STATUS_PATH} content mismatch.\nExpected: {expected}\nGot:      {data}"
    )


def test_metrics_json_content():
    """metrics.json must contain exactly the expected key/value pairs."""
    data = read_single_line_json(METRICS_PATH)
    expected = {"requests": 123, "errors": 0, "uptime": "48h"}
    assert data == expected, (
        f"{METRICS_PATH} content mismatch.\nExpected: {expected}\nGot:      {data}"
    )


def test_script_not_present_yet():
    """
    The automation script should NOT exist before the student’s action.
    Its presence would indicate the environment is not in the initial state.
    """
    assert not SCRIPT_PATH.exists(), f"Unexpected pre-existing script: {SCRIPT_PATH}"


def test_log_not_present_yet():
    """
    The log file should NOT exist before the student’s action.
    Its presence would indicate the environment is not in the initial state.
    """
    assert not LOG_PATH.exists(), f"Unexpected pre-existing log file: {LOG_PATH}"