# test_initial_state.py
#
# This pytest suite validates that the operating-system / filesystem
# is in the correct *initial* state **before** the student performs
# any action described in the task.  If any of these tests fail it
# means the workspace is not prepared as expected and the task should
# not proceed.

import json
from pathlib import Path

import pytest

# Constants
API_RESP_DIR = Path("/home/user/project/api_responses")
EXPECTED_JSON_FILES = [
    "response_200.json",
    "response_400.json",
    "response_500.json",
]
TEST_DIR = Path("/home/user/project/test")
RUN1_DIR = TEST_DIR / "run1"


def test_api_responses_directory_exists():
    """
    The directory /home/user/project/api_responses/ must exist.
    """
    assert API_RESP_DIR.is_dir(), (
        f"Expected directory {API_RESP_DIR} to exist, "
        "but it does not."
    )


def test_expected_json_files_present_and_only_those():
    """
    Verify that:
    1. Exactly the expected JSON files are present in
       /home/user/project/api_responses/.
    2. No additional *.json files exist.
    """
    present_files = sorted(
        p.name for p in API_RESP_DIR.glob("*.json") if p.is_file()
    )

    assert present_files == EXPECTED_JSON_FILES, (
        "Mismatch in JSON stubs inside "
        f"{API_RESP_DIR}.\n"
        f"Expected (ASCII-sorted): {EXPECTED_JSON_FILES}\n"
        f"Found               : {present_files}"
    )


@pytest.mark.parametrize("file_name,expected_status,expected_message", [
    ("response_200.json", 200, "OK"),
    ("response_400.json", 400, "Bad Request"),
    ("response_500.json", 500, "Server Error"),
])
def test_json_contents(file_name, expected_status, expected_message):
    """
    Ensure each JSON file is valid JSON and contains the expected
    'status' and 'message' values.  This guards against accidental
    corruption of the stub files.
    """
    file_path = API_RESP_DIR / file_name
    assert file_path.is_file(), f"Missing expected file: {file_path}"

    try:
        with file_path.open("r", encoding="utf-8") as fp:
            data = json.load(fp)
    except Exception as exc:  # pragma: no cover – any JSON error
        pytest.fail(f"{file_path} does not contain valid JSON: {exc}")

    assert data.get("status") == expected_status, (
        f"{file_path}: expected 'status' == {expected_status}, "
        f"found {data.get('status')!r}"
    )
    assert data.get("message") == expected_message, (
        f"{file_path}: expected 'message' == {expected_message!r}, "
        f"found {data.get('message')!r}"
    )


def test_test_and_run1_directories_do_not_exist_yet():
    """
    Before the student runs their solution no /home/user/project/test/
    (nor its subdirectory 'run1') should exist.
    """
    assert not TEST_DIR.exists(), (
        f"Directory {TEST_DIR} already exists; the workspace should "
        "start without it so the student can create it."
    )
    # RUN1_DIR is covered by the above assertion, but give a clearer message
    assert not RUN1_DIR.exists(), (
        f"Directory {RUN1_DIR} already exists; the student is expected "
        "to create it as part of the task."
    )