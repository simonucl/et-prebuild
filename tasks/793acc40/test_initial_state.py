# test_initial_state.py
#
# This test-suite validates the **initial** state of the operating system
# BEFORE the learner performs any action for the “pre-update diagnostic”
# task.  The presence of the required end-state artefacts at this point
# would indicate that the environment is not clean and would invalidate
# the exercise.

import os
from pathlib import Path

ROOT = Path("/home/user/rollout/logs")
STATUS_FILE = ROOT / "pre_update_system_status.log"


def test_rollout_directory_absence_or_clean_state():
    """
    The top-level directory for the task should not exist yet, or if it does
    exist it must not already contain the target log file.  This ensures that
    the learner starts from a clean slate.
    """
    if ROOT.exists():
        assert ROOT.is_dir(), (
            f"{ROOT} exists but is not a directory; "
            "please start with a clean environment."
        )
        # If the directory exists, the status file must NOT already be present.
        assert not STATUS_FILE.exists(), (
            f"Found unexpected pre-existing file: {STATUS_FILE}. "
            "The system should be in its pre-task state with no such file."
        )
    else:
        # Ideal clean start: the directory hierarchy is absent.
        assert not STATUS_FILE.exists(), (
            f"{STATUS_FILE} exists even though its parent directory "
            f"{ROOT} is missing.  Please remove the file for a clean start."
        )


def test_status_file_is_absent():
    """
    The specific log file must not exist before the learner creates it.
    """
    assert not STATUS_FILE.exists(), (
        f"Unexpected file detected: {STATUS_FILE}\n"
        "The log file should be created by the learner as part of the task, "
        "but it is already present."
    )