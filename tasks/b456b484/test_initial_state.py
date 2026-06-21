# test_initial_state.py
"""
Pytest suite to validate the initial workspace state *before* the student
executes any commands.

Checks performed:
1. /home/user/pipelines directory exists.
2. /home/user/pipelines/build-info.json file exists and is valid JSON.
3. build-info.json contains all required top-level keys:
   • build_id
   • commit_sha
   • artifact_url
   • status
4. /home/user/pipelines/README.txt file exists (mentioned as pre-existing, even
   though it is irrelevant for the task).

The suite purposefully does NOT test for any output files or directories
(e.g., /home/user/ci_reports) as per the specification.
"""

import json
import os
from pathlib import Path

import pytest

# Constants for full paths
PIPELINES_DIR = Path("/home/user/pipelines")
BUILD_INFO_JSON = PIPELINES_DIR / "build-info.json"
README_TXT = PIPELINES_DIR / "README.txt"

REQUIRED_KEYS = {"build_id", "commit_sha", "artifact_url", "status"}


def test_pipelines_directory_exists():
    assert PIPELINES_DIR.is_dir(), (
        f"Expected directory '{PIPELINES_DIR}' to exist, "
        "but it was not found."
    )


def test_build_info_file_exists():
    assert BUILD_INFO_JSON.is_file(), (
        f"Expected file '{BUILD_INFO_JSON}' to exist, "
        "but it was not found."
    )


def test_build_info_json_contains_required_keys():
    try:
        with open(BUILD_INFO_JSON, "r", encoding="utf-8") as fp:
            data = json.load(fp)
    except json.JSONDecodeError as exc:
        pytest.fail(
            f"File '{BUILD_INFO_JSON}' is not valid JSON: {exc}"
        )

    missing_keys = REQUIRED_KEYS - data.keys()
    assert not missing_keys, (
        "The following required keys are missing from "
        f"'{BUILD_INFO_JSON}': {', '.join(sorted(missing_keys))}"
    )


def test_readme_exists():
    assert README_TXT.is_file(), (
        f"Expected file '{README_TXT}' to exist, but it was not found."
    )