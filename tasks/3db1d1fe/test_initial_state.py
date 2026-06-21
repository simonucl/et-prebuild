# test_initial_state.py
"""
Pytest suite to verify the *initial* filesystem state **before** the student
performs any actions for the env-report task.

Truth requirements for the initial state:
1. /home/user/project               -> must already exist (it is the workspace)
2. /home/user/project/env_report    -> must NOT exist yet
3. /home/user/project/env_report/pip_packages.json -> must NOT exist yet
"""

import os
from pathlib import Path

PROJECT_DIR = Path("/home/user/project")
ENV_REPORT_DIR = PROJECT_DIR / "env_report"
PIP_JSON_FILE = ENV_REPORT_DIR / "pip_packages.json"


def test_project_directory_exists():
    """
    The project directory itself must be present; otherwise the student has
    nowhere to create the required env_report/ sub-directory.
    """
    assert PROJECT_DIR.exists(), (
        f"Expected project directory '{PROJECT_DIR}' to exist, "
        "but it is missing."
    )
    assert PROJECT_DIR.is_dir(), (
        f"Expected '{PROJECT_DIR}' to be a directory, "
        "but it is not a directory."
    )


def test_env_report_directory_absent_initially():
    """
    The env_report directory should NOT exist before the student executes
    their solution. Its presence would indicate leftover artifacts from a
    previous run.
    """
    assert not ENV_REPORT_DIR.exists(), (
        f"Directory '{ENV_REPORT_DIR}' should NOT exist yet. "
        "Remove it before running the task."
    )


def test_pip_packages_json_absent_initially():
    """
    Because the env_report directory itself must be absent, the JSON file inside
    it must also be absent. This explicit check yields a clearer error message
    if someone accidentally pre-creates just the file.
    """
    assert not PIP_JSON_FILE.exists(), (
        f"File '{PIP_JSON_FILE}' should NOT exist yet. "
        "It will be created by the student's command."
    )