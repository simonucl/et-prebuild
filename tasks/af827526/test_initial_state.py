# test_initial_state.py
#
# Pytest suite to verify that the system is in the expected **initial**
# (pre-task) state for the “deployment-logs” exercise.  None of the
# artefacts that the student is asked to create should exist yet.

import os
import stat
import pytest
from pathlib import Path

HOME = Path("/home/user")

DEPLOY_DIR = HOME / "deployment_logs"

# All artefacts that must NOT exist at the outset.
ARTEFACTS = [
    DEPLOY_DIR,
    DEPLOY_DIR / "pre_uptime.out",
    DEPLOY_DIR / "pre_df.out",
    DEPLOY_DIR / "pre_free.out",
    DEPLOY_DIR / "pre_ps.out",
    DEPLOY_DIR / "post_uptime.out",
    DEPLOY_DIR / "post_df.out",
    DEPLOY_DIR / "post_free.out",
    DEPLOY_DIR / "post_ps.out",
    DEPLOY_DIR / "summary.log",
    HOME / "dummy_update_marker.txt",
]


@pytest.mark.parametrize("path", ARTEFACTS)
def test_artefact_absence(path):
    """
    Ensure that none of the directories / files the student is supposed to
    create exist *before* the exercise begins.
    """
    assert not path.exists(), (
        f"Precondition failed: {path} already exists. "
        "The workspace must start clean so that the student "
        "can create this artefact during the exercise."
    )


def test_no_leftover_deployment_directory():
    """
    If /home/user/deployment_logs exists (perhaps owing to a previous run),
    fail early even if it is empty or has wrong permissions—students must
    create it afresh with the correct 0700 mode.
    """
    if DEPLOY_DIR.exists():
        # Directory is present when it should not be.  Supply a detailed reason.
        mode = stat.S_IMODE(DEPLOY_DIR.stat().st_mode)
        raise AssertionError(
            f"Precondition failed: {DEPLOY_DIR} unexpectedly exists with mode "
            f"{mode:04o}. Remove it before starting the task so that the "
            "student can create it with the required 0700 permissions."
        )