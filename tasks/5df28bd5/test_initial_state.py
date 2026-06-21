# test_initial_state.py
#
# Pytest suite that verifies the machine is in a clean *initial* state
# before the student starts working on the “process monitor” task.
#
# It checks that none of the expected *output* artefacts created by a
# successful solution are present yet.  If any of them already exist,
# the environment is considered “dirty” and the test fails with a clear
# explanation.
#
# Allowed imports: only stdlib + pytest.

import os
from pathlib import Path
import pytest

HOME = Path("/home/user")
MONITOR_DIR = HOME / "process_monitor"
USAGE_LOG = MONITOR_DIR / "usage_log.csv"
SUMMARY_TXT = MONITOR_DIR / "summary.txt"


@pytest.mark.describe("Initial filesystem state")
def test_usage_log_absent():
    """
    The sampling log must NOT exist before the student script runs.
    """
    assert not USAGE_LOG.exists(), (
        f"Found unexpected file at {USAGE_LOG}. "
        "The usage-log *must not* exist before you collect any samples. "
        "Remove it and start with a clean state."
    )


@pytest.mark.describe("Initial filesystem state")
def test_summary_txt_absent():
    """
    The statistics summary must NOT exist before the student script runs.
    """
    assert not SUMMARY_TXT.exists(), (
        f"Found unexpected file at {SUMMARY_TXT}. "
        "The summary file should only be generated *after* sampling. "
        "Delete it to begin with a fresh environment."
    )


@pytest.mark.describe("Initial filesystem state")
def test_directory_does_not_contain_output_files():
    """
    The target directory may or may not exist yet, but if it does
    it must not contain either of the required output files.
    """
    if MONITOR_DIR.is_dir():
        offending = [
            str(p) for p in (MONITOR_DIR.iterdir())
            if p.name in {USAGE_LOG.name, SUMMARY_TXT.name}
        ]
        assert not offending, (
            "The directory /home/user/process_monitor already exists and "
            f"contains unexpected output files: {', '.join(offending)}. "
            "Start with an empty directory or remove these files."
        )