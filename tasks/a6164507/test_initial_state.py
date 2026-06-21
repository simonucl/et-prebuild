# test_initial_state.py
"""
Pytest suite that validates the initial filesystem/OS state **before** the student
runs any commands for the IoT-rollout task.

The tests assert:
1. /home/user/deployment exists, is a directory and has mode >= 0755.
2. /home/user/deployment/edge_device_config.json exists, is a regular file,
   and its bytes match the specification exactly.
3. /home/user/deployment/validation_report.txt must NOT exist yet.
4. The JSON content is indeed a top-level list whose length is 5.
"""

import json
import os
import stat
from pathlib import Path

DEPLOY_DIR = Path("/home/user/deployment")
CONFIG_PATH = DEPLOY_DIR / "edge_device_config.json"
REPORT_PATH = DEPLOY_DIR / "validation_report.txt"

EXPECTED_JSON_TEXT = (
    "[\n"
    "  {\"id\":\"dev-001\",\"location\":\"NYC\",\"status\":\"active\"},\n"
    "  {\"id\":\"dev-002\",\"location\":\"Berlin\",\"status\":\"inactive\"},\n"
    "  {\"id\":\"dev-003\",\"location\":\"London\",\"status\":\"active\"},\n"
    "  {\"location\":\"Tokyo\",\"status\":\"inactive\"},\n"
    "  {\"id\":\"dev-005\",\"location\":\"Paris\",\"status\":\"inactive\"}\n"
    "]\n"
)


def _octal_mode(path: Path) -> int:
    """Return the file’s permission bits in octal, e.g. 0o755."""
    return stat.S_IMODE(path.stat().st_mode)


def test_deployment_directory_exists_and_permissions():
    assert DEPLOY_DIR.exists(), f"Required directory {DEPLOY_DIR} is missing."
    assert DEPLOY_DIR.is_dir(), f"{DEPLOY_DIR} exists but is not a directory."
    mode = _octal_mode(DEPLOY_DIR)
    assert mode >= 0o755, (
        f"Directory {DEPLOY_DIR} has permissions {oct(mode)}, expected at least 0o755."
    )


def test_edge_device_config_file_exact_contents_and_permissions():
    assert CONFIG_PATH.exists(), f"Required file {CONFIG_PATH} is missing."
    assert CONFIG_PATH.is_file(), f"{CONFIG_PATH} exists but is not a regular file."

    # Validate exact byte-for-byte content.
    actual_text = CONFIG_PATH.read_text(encoding="utf-8")
    assert (
        actual_text == EXPECTED_JSON_TEXT
    ), f"Content of {CONFIG_PATH} does not match the expected specification."

    # Sanity-check permissions: file must be readable.
    mode = _octal_mode(CONFIG_PATH)
    assert mode & stat.S_IRUSR, f"{CONFIG_PATH} is not readable by the owner."


def test_json_is_top_level_array_of_five_elements():
    data = json.loads(EXPECTED_JSON_TEXT)
    assert isinstance(
        data, list
    ), "The JSON content should be a top-level array but is not."
    assert (
        len(data) == 5
    ), f"The JSON array should contain 5 elements, found {len(data)}."


def test_validation_report_must_not_exist_yet():
    assert (
        not REPORT_PATH.exists()
    ), f"{REPORT_PATH} should NOT exist before the student runs their command."