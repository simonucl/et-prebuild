# test_initial_state.py
#
# This test-suite validates the *initial* filesystem state **before**
# the student starts working on the assignment.  It ensures that
# 1. The expected source directory and CSV extracts are present and correct.
# 2. No compliance artefacts (directory or files) are present yet.
#
# Only the Python stdlib and pytest are used.

import os
from pathlib import Path
import pytest

RAW_DIR = Path("/home/user/raw")
COMPLIANCE_DIR = Path("/home/user/compliance")

RAW_FILES = {
    "hostnames.csv": [
        "HOSTNAME\n",
        "server01\n",
        "server02\n",
        "db01\n",
        "web02\n",
        "proxy01\n",
    ],
    "os.csv": [
        "OS\n",
        "Ubuntu 20.04\n",
        "CentOS 8\n",
        "Ubuntu 18.04\n",
        "Debian 10\n",
        "AlmaLinux 9\n",
    ],
    "patch_status.csv": [
        "PATCH_STATUS\n",
        "Compliant\n",
        "Non-Compliant\n",
        "Compliant\n",
        "Compliant\n",
        "Non-Compliant\n",
    ],
    "av_status.csv": [
        "AV_STATUS\n",
        "Enabled\n",
        "Disabled\n",
        "Enabled\n",
        "Enabled\n",
        "Disabled\n",
    ],
}

@pytest.mark.parametrize("filename", RAW_FILES.keys())
def test_raw_files_exist(filename):
    """Each required raw CSV file must exist in /home/user/raw."""
    full_path = RAW_DIR / filename
    assert full_path.exists(), f"Missing required file: {full_path}"
    assert full_path.is_file(), f"Path exists but is not a file: {full_path}"


def _read_lines(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        return fh.readlines()


@pytest.mark.parametrize("filename,expected_lines", RAW_FILES.items())
def test_raw_file_contents(filename, expected_lines):
    """
    Verify that every raw CSV file contains exactly the expected
    six lines (header + 5 data rows) _before_ any student processing.
    """
    path = RAW_DIR / filename
    lines = _read_lines(path)

    assert lines == expected_lines, (
        f"File {path} does not match the expected initial contents.\n"
        "If this file has already been modified, revert it to the original "
        "state before starting the exercise."
    )


def test_raw_directory_properties():
    """The /home/user/raw directory itself must exist and be a directory."""
    assert RAW_DIR.exists(), f"Required directory missing: {RAW_DIR}"
    assert RAW_DIR.is_dir(), f"{RAW_DIR} exists but is not a directory"


def test_compliance_directory_absent():
    """
    Before the student starts, the compliance directory should **not**
    exist.  Its creation is part of the exercise.
    """
    assert not COMPLIANCE_DIR.exists(), (
        f"The directory {COMPLIANCE_DIR} already exists. "
        "Please start with a clean slate."
    )


@pytest.mark.parametrize(
    "path",
    [
        COMPLIANCE_DIR / "final_audit.csv",
        COMPLIANCE_DIR / "generation.log",
    ],
)
def test_output_files_absent(path):
    """No output artefacts should exist yet."""
    assert not path.exists(), (
        f"Output file {path} should not be present before the assignment "
        "has been completed."
    )