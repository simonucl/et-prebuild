# test_initial_state.py
#
# Pytest suite that validates the operating-system / filesystem **before**
# the student script runs.  It confirms that the mock API data are present
# with the correct contents, and that the writable log directory exists
# but contains no log file yet.
#
# Only the Python standard library and pytest are used.

import json
import os
from pathlib import Path

import pytest

HOME = Path("/home/user").resolve()
MOCK_API_ROOT = HOME / "mock_api"
TICKET_LOG_DIR = HOME / "ticket_logs"

# Expected mock-API structure and contents
EXPECTED_FILES = {
    "auth": {
        "path": MOCK_API_ROOT / "auth" / "status.json",
        "json": {"service": "auth", "status": "ok"},
    },
    "files": {
        "path": MOCK_API_ROOT / "files" / "status.json",
        "json": {"service": "files", "status": "ok"},
    },
    "billing": {
        "path": MOCK_API_ROOT / "billing" / "status.json",
        "json": {"service": "billing", "status": "degraded"},
    },
}


@pytest.mark.parametrize("service", EXPECTED_FILES.keys())
def test_mock_api_files_exist_with_correct_content(service):
    """
    Verify that each /home/user/mock_api/<service>/status.json file exists
    and contains the exact JSON expected by the exercise description.
    """
    file_info = EXPECTED_FILES[service]
    file_path = file_info["path"]

    # 1. Path existence and type checks
    assert file_path.parent.is_dir(), (
        f"Missing directory: {file_path.parent}. "
        "Each service should have its own directory under /home/user/mock_api/."
    )
    assert file_path.is_file(), (
        f"Missing file: {file_path}. "
        "The mock API must provide status.json for every service."
    )

    # 2. File content check
    try:
        with file_path.open("r", encoding="utf-8") as fp:
            data = json.load(fp)
    except json.JSONDecodeError as exc:
        pytest.fail(f"{file_path} does not contain valid JSON: {exc}")

    assert data == file_info["json"], (
        f"Unexpected content in {file_path}.\n"
        f"Expected: {file_info['json']}\n"
        f"Found:    {data}"
    )


def test_mock_api_root_dir_exists():
    """
    Ensure the top-level mock API directory exists.
    """
    assert MOCK_API_ROOT.is_dir(), (
        f"Required directory {MOCK_API_ROOT} is missing. "
        "All mock API data should live under this path."
    )


def test_ticket_log_directory_is_ready_and_empty():
    """
    The /home/user/ticket_logs/ directory must exist and be empty before
    the student produces the service_checks.log file.
    """
    assert TICKET_LOG_DIR.is_dir(), (
        f"Missing directory: {TICKET_LOG_DIR}. "
        "Create it so that the final log file can be written there."
    )

    contents = list(TICKET_LOG_DIR.iterdir())
    assert contents == [], (
        f"{TICKET_LOG_DIR} is expected to be empty at the start, "
        f"but it already contains: {', '.join(str(p) for p in contents)}"
    )