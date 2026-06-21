# test_initial_state.py
#
# Pytest suite that verifies the operating-system / filesystem state
# *before* the student performs any action for the “jq one-liner” task.
#
# The checks assert the following:
#   1. The directory /home/user/storage exists and is readable.
#   2. The file  /home/user/storage/disks.json exists, has mode 0644,
#      contains valid JSON, and every top-level element is an object
#      with both a string “name” and a numeric “size_gb”.
#   3. The directory /home/user/reports exists, has mode 0755,
#      and is currently empty (the student will create the log file
#      inside this directory later).
#   4. The executable “jq” is available in $PATH so the student can
#      fulfil the one-liner requirement.
#
# No assertions are made about the output file
# /home/user/reports/disk_validation.log, because it must NOT exist yet.

import json
import os
import stat
import subprocess
import sys
from pathlib import Path

STORAGE_DIR = Path("/home/user/storage")
REPORTS_DIR = Path("/home/user/reports")
DISKS_JSON = STORAGE_DIR / "disks.json"


def _octal_mode(path: Path) -> int:
    """Return the Unix permission bits of `path` as an octal integer (e.g. 0o644)."""
    return stat.S_IMODE(path.stat().st_mode)


def test_storage_directory_exists_and_permissions():
    assert STORAGE_DIR.exists(), f"Required directory {STORAGE_DIR} is missing."
    assert STORAGE_DIR.is_dir(), f"{STORAGE_DIR} exists but is not a directory."
    expected_mode = 0o755
    actual_mode = _octal_mode(STORAGE_DIR)
    assert (
        actual_mode == expected_mode
    ), f"{STORAGE_DIR} permissions are {oct(actual_mode)}, expected {oct(expected_mode)}."


def test_reports_directory_exists_is_empty_and_permissions():
    assert REPORTS_DIR.exists(), f"Required directory {REPORTS_DIR} is missing."
    assert REPORTS_DIR.is_dir(), f"{REPORTS_DIR} exists but is not a directory."

    # It must be empty before the student writes the log file.
    contents = os.listdir(REPORTS_DIR)
    assert (
        len(contents) == 0
    ), f"{REPORTS_DIR} should be empty before the task begins, found: {contents}"

    expected_mode = 0o755
    actual_mode = _octal_mode(REPORTS_DIR)
    assert (
        actual_mode == expected_mode
    ), f"{REPORTS_DIR} permissions are {oct(actual_mode)}, expected {oct(expected_mode)}."


def test_disks_json_file_exists_and_permissions():
    assert DISKS_JSON.exists(), f"Required file {DISKS_JSON} is missing."
    assert DISKS_JSON.is_file(), f"{DISKS_JSON} exists but is not a regular file."
    expected_mode = 0o644
    actual_mode = _octal_mode(DISKS_JSON)
    assert (
        actual_mode == expected_mode
    ), f"{DISKS_JSON} permissions are {oct(actual_mode)}, expected {oct(expected_mode)}."


def test_disks_json_content_is_valid_and_compliant():
    try:
        with DISKS_JSON.open("r", encoding="utf-8") as fp:
            data = json.load(fp)
    except json.JSONDecodeError as exc:
        raise AssertionError(f"{DISKS_JSON} is not valid JSON: {exc}") from None

    assert isinstance(
        data, list
    ), f"{DISKS_JSON} must contain a JSON array at the top level, got {type(data).__name__}."

    assert (
        len(data) > 0
    ), f"{DISKS_JSON} should contain at least one disk object, found an empty array."

    for idx, item in enumerate(data):
        assert isinstance(
            item, dict
        ), f"Element {idx} in {DISKS_JSON} should be an object, got {type(item).__name__}."

        missing = {"name", "size_gb"} - item.keys()
        assert (
            not missing
        ), f"Element {idx} in {DISKS_JSON} is missing required keys: {missing}"

        assert isinstance(
            item["name"], str
        ), f"Element {idx} key 'name' should be a string, got {type(item['name']).__name__}."

        assert isinstance(
            item["size_gb"], (int, float)
        ), f"Element {idx} key 'size_gb' should be numeric, got {type(item['size_gb']).__name__}."


def test_jq_is_available():
    """Ensure that the 'jq' executable is present in the environment PATH."""
    jq_path = subprocess.run(
        ["which", "jq"], capture_output=True, text=True, check=False
    ).stdout.strip()

    assert jq_path, (
        "'jq' executable not found in PATH. It is required for the one-liner solution."
    )

    # Additionally, ensure that the found path is executable.
    assert os.access(
        jq_path, os.X_OK
    ), f"'jq' found at {jq_path} but it is not executable."


# Collect all tests for explicit exported names when pytest -q is used
__all__ = [
    "test_storage_directory_exists_and_permissions",
    "test_reports_directory_exists_is_empty_and_permissions",
    "test_disks_json_file_exists_and_permissions",
    "test_disks_json_content_is_valid_and_compliant",
    "test_jq_is_available",
]