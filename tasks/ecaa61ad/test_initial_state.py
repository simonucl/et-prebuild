# test_initial_state.py
#
# This pytest suite verifies that the starting file-system state required by the
# assignment is present and correct.  It *only* checks the pre-existing inputs
# (JSON mock API responses).  It intentionally does NOT look for the output
# directory or any artefacts that the student is expected to create later.

import json
import pathlib
import pytest

HOME = pathlib.Path("/home/user")
RESP_DIR = HOME / "api_responses"

# --------------------------------------------------------------------------- #
# Helper data that encodes the exact ground-truth we expect to find on disk.
# --------------------------------------------------------------------------- #
EXPECTED_FILES = {
    "response_1.json": {"id": 101, "status": "OK",   "latency_ms": 234},
    "response_2.json": {"id": 102, "status": "FAIL", "latency_ms": 678},
    "response_3.json": {"id": 103, "status": "OK",   "latency_ms": 345},
}


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_responses_directory_exists():
    """
    The directory /home/user/api_responses must exist and be a directory.
    """
    assert RESP_DIR.exists(), f"Required directory {RESP_DIR} is missing."
    assert RESP_DIR.is_dir(), f"{RESP_DIR} exists but is not a directory."


def test_expected_files_present_and_no_extras():
    """
    Exactly the three expected JSON files must be present—no more, no fewer.
    """
    on_disk = {p.name for p in RESP_DIR.glob("response_*.json")}
    expected = set(EXPECTED_FILES.keys())

    missing = expected - on_disk
    unexpected = on_disk - expected

    assert not missing, (
        "The following required JSON files are missing:\n"
        + "\n".join(sorted(missing))
    )
    assert not unexpected, (
        "Unexpected JSON files found in the api_responses directory:\n"
        + "\n".join(sorted(unexpected))
    )


@pytest.mark.parametrize("filename, expected_payload", EXPECTED_FILES.items())
def test_each_json_file_has_correct_payload(filename, expected_payload):
    """
    Each JSON file must contain the exact id, status, and latency_ms fields
    specified by the assignment.
    """
    file_path = RESP_DIR / filename
    assert file_path.exists(), f"Expected file {file_path} is missing."

    # Read & parse JSON
    try:
        data = json.loads(file_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        pytest.fail(f"File {file_path} is not valid JSON: {e}")

    # Verify that all required keys are present
    for key in ("id", "status", "latency_ms"):
        assert key in data, f"Key '{key}' missing in {file_path}."

    # Compare the entire payload for strict equality
    assert data == expected_payload, (
        f"Content mismatch in {file_path}.\n"
        f"Expected: {expected_payload!r}\n"
        f"Found:    {data!r}"
    )