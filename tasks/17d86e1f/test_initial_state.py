# test_initial_state.py
#
# Pytest suite that validates the **initial** state of the filesystem
# before the student runs any solution code for the “compress-oversized
# JSON files” exercise.
#
# The checks assert:
#   • Required directories are present with 0700 permissions.
#   • Specific “*.json” files exist with the exact sizes prescribed in
#     the task description.
#   • No “*.json.gz” counterparts exist yet.
#   • /home/user/cloud_costs/compression_report.csv is absent.
#
# Only the Python standard library and pytest are used.

import os
import stat
import pytest

DIR_COSTS = "/home/user/cloud_costs"
DIR_RAW   = "/home/user/cloud_costs/raw_usage"

# Expected files and their sizes (bytes) **before** the student acts.
OVERSIZED_JSONS = {
    "/home/user/cloud_costs/raw_usage/2023-11-01-usage.json": 2_097_152,  # 2 MiB
    "/home/user/cloud_costs/raw_usage/2024-01-01-usage.json": 3_145_728,  # 3 MiB
    "/home/user/cloud_costs/raw_usage/2024-01-15-usage.json": 1_245_184,  # ≈1.188 MiB
}

SMALL_JSON = {
    "/home/user/cloud_costs/raw_usage/2023-12-01-usage.json": 512_000,
}

REPORT_PATH = "/home/user/cloud_costs/compression_report.csv"

ALL_EXPECTED_JSONS = {**OVERSIZED_JSONS, **SMALL_JSON}


def _file_size(path):
    return os.stat(path).st_size


def _perm(path):
    """Return permission bits as an int in the range 0-0o777."""
    return stat.S_IMODE(os.stat(path).st_mode)


def test_required_directories_exist_with_permissions():
    for directory in (DIR_COSTS, DIR_RAW):
        assert os.path.isdir(directory), (
            f"Required directory {directory!r} is missing."
        )
        perms = _perm(directory)
        assert perms == 0o700, (
            f"Directory {directory!r} must have 0700 permissions; "
            f"found {oct(perms)} instead."
        )


@pytest.mark.parametrize("json_path,expected_size", OVERSIZED_JSONS.items())
def test_oversized_json_files_present_with_exact_size(json_path, expected_size):
    assert os.path.isfile(json_path), (
        f"Oversized JSON file {json_path!r} is missing."
    )
    actual_size = _file_size(json_path)
    assert actual_size == expected_size, (
        f"File {json_path!r} should be {expected_size} bytes; "
        f"found {actual_size} bytes."
    )
    assert actual_size > 1_048_576, (
        f"File {json_path!r} was expected to exceed 1 MiB but is "
        f"only {actual_size} bytes."
    )
    gz_path = f"{json_path}.gz"
    assert not os.path.exists(gz_path), (
        f"Compressed counterpart {gz_path!r} should NOT exist yet."
    )


@pytest.mark.parametrize("json_path,expected_size", SMALL_JSON.items())
def test_small_json_file_present_and_below_threshold(json_path, expected_size):
    assert os.path.isfile(json_path), (
        f"Small JSON file {json_path!r} is missing."
    )
    actual_size = _file_size(json_path)
    assert actual_size == expected_size, (
        f"File {json_path!r} should be {expected_size} bytes; "
        f"found {actual_size} bytes."
    )
    assert actual_size < 1_048_576, (
        f"File {json_path!r} should be below 1 MiB; "
        f"found {actual_size} bytes."
    )
    gz_path = f"{json_path}.gz"
    assert not os.path.exists(gz_path), (
        f"Compressed counterpart {gz_path!r} should NOT exist yet."
    )


def test_no_unexpected_json_files():
    """
    Ensure that the raw_usage directory contains exactly the JSON files
    specified in the initial state (no stragglers that could interfere
    with grading).
    """
    present_jsons = sorted(
        f for f in os.listdir(DIR_RAW)
        if f.endswith(".json")
    )
    expected_jsons = sorted(
        os.path.basename(p) for p in ALL_EXPECTED_JSONS
    )
    assert present_jsons == expected_jsons, (
        "Unexpected *.json files detected in "
        f"{DIR_RAW!r}. Expected:\n  {expected_jsons}\nFound:\n  {present_jsons}"
    )


def test_compression_report_absent_initially():
    assert not os.path.exists(REPORT_PATH), (
        f"{REPORT_PATH!r} should NOT exist before the student runs their "
        "solution."
    )