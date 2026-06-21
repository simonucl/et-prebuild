# test_initial_state.py
#
# This pytest suite verifies that the system is still in its pristine
# “pre-task” state.  None of the artefacts that the student is expected
# to create during the exercise should exist yet.  If any of them are
# found, the tests will fail with a clear, actionable message.
#
# Checked paths (all MUST be absent prior to student action):
#   • /home/user/diagnostics                     (directory)
#   • /home/user/diagnostics/summary.log         (file)
#   • /home/user/diagnostics/diagnostics_bundle.tar.gz  (file)

import os
import pytest
from pathlib import Path


DIAG_DIR = Path("/home/user/diagnostics")
SUMMARY_LOG = DIAG_DIR / "summary.log"
BUNDLE = DIAG_DIR / "diagnostics_bundle.tar.gz"


def _human(path: Path) -> str:
    """Return a human-readable representation of the path."""
    return str(path)


@pytest.mark.order(1)
def test_diagnostics_directory_absent():
    """
    /home/user/diagnostics must NOT exist before the student runs their solution.
    """
    assert not DIAG_DIR.exists(), (
        f"The directory {_human(DIAG_DIR)} already exists. "
        "The exercise requires you to create it; please ensure you start from a clean state."
    )


@pytest.mark.order(2)
def test_summary_log_absent():
    """
    /home/user/diagnostics/summary.log must NOT exist before the student runs their solution.
    """
    assert not SUMMARY_LOG.exists(), (
        f"The file {_human(SUMMARY_LOG)} is present but should not be. "
        "Remove it before starting the task so the test harness can verify your work."
    )


@pytest.mark.order(3)
def test_bundle_absent():
    """
    /home/user/diagnostics/diagnostics_bundle.tar.gz must NOT exist before the student runs their solution.
    """
    assert not BUNDLE.exists(), (
        f"The archive {_human(BUNDLE)} already exists. "
        "This file should only be created as part of the task; "
        "please clean up any leftovers from previous attempts."
    )