# test_initial_state.py
#
# This pytest file validates the machine *before* the student starts
# working on the “Loopback Interface Sanity Check” task.  The checks
# confirm that no artefacts from a previous run are already present.
#
# If any of these tests fail it means the environment is not in the
# pristine state expected by the assignment specification.

import os
from pathlib import Path

import pytest

# Constants for expected paths -------------------------------------------------
BASE_DIR = Path("/home/user")
DIAG_DIR = BASE_DIR / "network_diagnostics"
DIAG_LOG = DIAG_DIR / "diagnostics.log"


@pytest.mark.describe("Pre-exercise filesystem sanity")
class TestInitialState:
    def test_network_diagnostics_directory_must_not_exist(self):
        """
        The directory /home/user/network_diagnostics must NOT exist before the
        student begins.  Its presence would indicate that the workspace is
        dirty (perhaps from an earlier attempt).
        """
        if DIAG_DIR.exists():
            # Provide a detailed explanation so the learner knows what to fix.
            is_dir = DIAG_DIR.is_dir()
            pytest.fail(
                f"The path {DIAG_DIR} already exists and {'is' if is_dir else 'is NOT'} "
                f"a directory.  Please remove it or start from a clean workspace "
                f"before beginning the assignment."
            )

    def test_diagnostics_log_must_not_exist(self):
        """
        The log file /home/user/network_diagnostics/diagnostics.log must NOT
        exist before the student begins.  The assignment requires the student
        to create the file from scratch.
        """
        if DIAG_LOG.exists():
            pytest.fail(
                f"The file {DIAG_LOG} already exists.  The workspace must be clean "
                f"before starting the assignment."
            )