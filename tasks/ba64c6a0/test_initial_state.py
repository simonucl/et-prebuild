# test_initial_state.py
#
# This pytest suite validates the **initial** state of the operating system
# before the student starts working on “Stage a Firewall Roll-out Package for
# the Ops Team”.
#
# Nothing related to the target deliverables should exist yet.  In particular
# the directory `/home/user/deployment/firewall` **must not** be present and
# none of the four required files may exist.  These tests fail early and with
# clear messages if any artefact is found.

import os
import pytest
from pathlib import Path

# Base directory constants
HOME = Path("/home/user")
DEPLOY_DIR = HOME / "deployment"
FIREWALL_DIR = DEPLOY_DIR / "firewall"

# All files that should *not* be present at the beginning
EXPECTED_FILES = [
    FIREWALL_DIR / "iptables_v4.rules",
    FIREWALL_DIR / "iptables_v6.rules",
    FIREWALL_DIR / "firewall_summary.json",
    FIREWALL_DIR / "config_audit.log",
]

@pytest.mark.describe("Pre-exercise filesystem state")
class TestInitialState:
    def test_firewall_directory_absent(self):
        """
        The directory /home/user/deployment/firewall must not exist yet.
        """
        assert not FIREWALL_DIR.exists(), (
            f"Directory {FIREWALL_DIR} already exists. "
            "The task requires the student to create it."
        )

    @pytest.mark.parametrize("file_path", EXPECTED_FILES)
    def test_no_expected_files_exist(self, file_path: Path):
        """
        None of the deliverable files may exist before the student starts.
        """
        assert not file_path.exists(), (
            f"Found unexpected file {file_path}. "
            "The working directory should be clean before starting the task."
        )