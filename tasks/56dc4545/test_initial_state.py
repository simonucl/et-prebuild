# test_initial_state.py
#
# This pytest suite validates that the workspace is still **pristine**
# before the student starts solving the exercise.  None of the target
# artefacts for the firewall task should exist at this point.

import os
from pathlib import Path
import pytest

# Base directory and artefact paths that must NOT exist yet
BASE_DIR = Path("/home/user/ml_firewall")
FILES = {
    "firewall_rules.conf": BASE_DIR / "firewall_rules.conf",
    "apply_firewall.sh":   BASE_DIR / "apply_firewall.sh",
    "firewall_changes.log":BASE_DIR / "firewall_changes.log",
}


def test_home_directory_present():
    """Sanity-check that /home/user itself exists; otherwise the test
    environment is broken."""
    home = Path("/home/user")
    assert home.exists() and home.is_dir(), (
        "Expected base home directory /home/user to exist for the exercise."
    )


def test_ml_firewall_directory_absent():
    """The dedicated ml_firewall directory must NOT exist yet."""
    assert not BASE_DIR.exists(), (
        "Directory /home/user/ml_firewall already exists. "
        "The workspace should be clean before the student starts."
    )


@pytest.mark.parametrize("file_name,file_path", FILES.items())
def test_target_files_absent(file_name, file_path):
    """None of the target files should be present before the student works."""
    assert not file_path.exists(), (
        f"File {file_path} unexpectedly exists. "
        "The student must create this file during the exercise, "
        "so it should be absent at the outset."
    )