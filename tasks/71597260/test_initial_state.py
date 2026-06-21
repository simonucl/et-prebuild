# test_initial_state.py
#
# This pytest suite validates the *initial* state of the operating-system
# before the student begins the task.  It guarantees that nothing from a
# previous run (e.g., an existing /home/user/pt_scan directory or
# tcp_listen.log file) is present, so the exercise starts from a clean slate.

import os
from pathlib import Path

HOME_DIR         = Path("/home/user")
PT_SCAN_DIR      = HOME_DIR / "pt_scan"
TCP_LISTEN_LOG   = PT_SCAN_DIR / "tcp_listen.log"


def test_home_directory_exists():
    """The base home directory must exist and be a directory."""
    assert HOME_DIR.exists(), f"Expected {HOME_DIR} to exist."
    assert HOME_DIR.is_dir(), f"Expected {HOME_DIR} to be a directory."


def test_pt_scan_directory_absent():
    """
    The /home/user/pt_scan directory should NOT exist at the start.
    The student will create it (if absent) as part of the task.
    """
    assert not PT_SCAN_DIR.exists(), (
        f"Pre-condition failure: {PT_SCAN_DIR} already exists. "
        "The workspace must start clean so the student can create it."
    )


def test_tcp_listen_log_absent():
    """
    The target log file must not be present yet.  It will be generated
    by the student's compound shell command.
    """
    assert not TCP_LISTEN_LOG.exists(), (
        f"Pre-condition failure: {TCP_LISTEN_LOG} already exists. "
        "Remove it so the task begins with no prior artifacts."
    )