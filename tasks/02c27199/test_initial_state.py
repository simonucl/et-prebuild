# test_initial_state.py
#
# This pytest suite validates the *initial* operating-system / filesystem state
# before the student performs any actions for the “DevSecOps policy-as-code”
# exercise.

import os
from pathlib import Path
import pytest

# Fixed, absolute paths used throughout the assignment
PROJECT_ROOT = Path("/home/user/devsecops-policy")
ALLOW_LIST_FILE = PROJECT_ROOT / "allowed_packages.txt"
VENV_DIR = PROJECT_ROOT / "venv"
LOGS_DIR = PROJECT_ROOT / "logs"
COMPLIANCE_REPORT = LOGS_DIR / "compliance_report.csv"

EXPECTED_ALLOW_LIST_CONTENT = "requests==2.31.0\n"


def test_allow_list_file_exists_with_exact_content():
    """
    The allow-list file must exist **before** the student starts and must contain
    exactly one line: 'requests==2.31.0' followed by a newline.
    """
    assert ALLOW_LIST_FILE.is_file(), (
        f"Required allow-list file missing at: {ALLOW_LIST_FILE}"
    )

    actual = ALLOW_LIST_FILE.read_text(encoding="utf-8")
    assert actual == EXPECTED_ALLOW_LIST_CONTENT, (
        "allow-list file content is incorrect.\n"
        f"Expected EXACTLY:\n{repr(EXPECTED_ALLOW_LIST_CONTENT)}\n"
        f"Got:\n{repr(actual)}"
    )


def test_virtualenv_does_not_exist_yet():
    """
    No virtual environment should exist prior to the student's actions.
    """
    assert not VENV_DIR.exists(), (
        f"Virtual environment directory should NOT exist yet, but found: {VENV_DIR}"
    )


def test_compliance_report_absent_initially():
    """
    The compliance report should not be present before the student generates it.
    """
    assert not COMPLIANCE_REPORT.exists(), (
        "Compliance report already exists; the student must generate it themselves."
    )
    # It's acceptable for the logs directory to exist or not; only the report
    # must be absent. If we want stricter checks, uncomment the next two lines.
    # assert not LOGS_DIR.exists(), (
    #     f"'logs' directory should not exist yet, but found: {LOGS_DIR}"
    # )