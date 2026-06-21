# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem
# state for the “mock_api” DevOps exercise.
#
# The tests confirm that:
#   1. All required seed files and directories are present under
#      /home/user/mock_api.
#   2. Each file contains the exact, canonical content that the
#      subsequent assignment relies on.
#   3. Essential CLI tools (curl & jq) are available in the PATH.
#
# Nothing related to the *output* (/home/user/logs …) is tested here, in
# strict accordance with the grading rubric.

import json
import shutil
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

HOME = Path("/home/user")
API_DIR = HOME / "mock_api"

INVENTORY_FILE = API_DIR / "inventory.json"
USER_FILE = API_DIR / "user.json"
HEALTH_FILE = API_DIR / "health.txt"

# Canonical JSON / text expected in the seed resources
EXPECTED_INVENTORY = {
    "total_items": 3,
    "items": ["widget", "gadget", "doodad"],
}

EXPECTED_USER = {
    "users": [
        {"id": 1, "username": "alice"},
        {"id": 2, "username": "bob"},
    ]
}

EXPECTED_HEALTH_CONTENT = "OK\n"


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _read_json(path: Path):
    """Return parsed JSON, raising a helpful assertion if the file is empty
    or malformed."""
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        pytest.fail(f"Required file is missing: {path}")

    if not text.strip():
        pytest.fail(f"File {path} is empty; expected valid JSON.")

    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        pytest.fail(f"File {path} does not contain valid JSON: {exc}")


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_api_directory_exists():
    assert API_DIR.is_dir(), (
        f"Directory {API_DIR} must exist and be a directory. "
        "This directory should contain the seed API resources."
    )


def test_inventory_json_exists_and_content():
    assert INVENTORY_FILE.is_file(), (
        f"Missing required file: {INVENTORY_FILE}"
    )

    data = _read_json(INVENTORY_FILE)
    assert data == EXPECTED_INVENTORY, (
        f"{INVENTORY_FILE} contents do not match the expected seed data.\n"
        f"Expected: {EXPECTED_INVENTORY}\n"
        f"Found:    {data}"
    )


def test_user_json_exists_and_content():
    assert USER_FILE.is_file(), (
        f"Missing required file: {USER_FILE}"
    )

    data = _read_json(USER_FILE)
    assert data == EXPECTED_USER, (
        f"{USER_FILE} contents do not match the expected seed data.\n"
        f"Expected: {EXPECTED_USER}\n"
        f"Found:    {data}"
    )


def test_health_txt_exists_and_content():
    assert HEALTH_FILE.is_file(), (
        f"Missing required file: {HEALTH_FILE}"
    )

    raw_text = HEALTH_FILE.read_text(encoding="utf-8")
    assert raw_text == EXPECTED_HEALTH_CONTENT, (
        f"{HEALTH_FILE} must contain exactly 'OK' followed by a single LF.\n"
        f"Expected repr: {repr(EXPECTED_HEALTH_CONTENT)}\n"
        f"Found repr:    {repr(raw_text)}"
    )


@pytest.mark.parametrize("binary", ["curl", "jq"])
def test_required_cli_tools_present(binary):
    """Ensure that 'curl' and 'jq' are available in the PATH.

    The assignment explicitly instructs students to use these tools, so
    they must be present for the exercise to be solvable.
    """
    path = shutil.which(binary)
    assert path is not None, (
        f"Required command-line tool '{binary}' is not available in PATH. "
        f"Please ensure it is installed and accessible."
    )