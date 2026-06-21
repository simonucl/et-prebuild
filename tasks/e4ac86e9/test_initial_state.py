# test_initial_state.py
#
# This pytest file verifies that none of the artefacts required by the
# assignment exist *before* the student starts working.  The environment
# must be clean so that the follow-up “solution” test suite can determine
# whether the student really created everything themselves.

import os
import stat
import pytest
from pathlib import Path

HOME = Path("/home/user")
ENV_DIR = HOME / "alerts_env"
ENV_PYTHON = ENV_DIR / "bin" / "python"
REPORT_LOG = HOME / "alerts_report.log"
SUMMARY_TXT = HOME / "alerts_summary.txt"


def _should_not_exist(path: Path) -> None:
    """
    Helper that asserts the given path does *not* exist, with a clear
    failure explanation.
    """
    assert not path.exists(), (
        f"Pre-exercise sanity check failed: {path} already exists, "
        "but the student is expected to create it as part of the task. "
        "Remove the path before you begin."
    )


def test_home_directory_is_present_and_writable():
    """
    Basic sanity check: /home/user must exist and be writable so the
    student can place new files and directories there.
    """
    assert HOME.is_dir(), "/home/user is missing; the testing environment is broken."
    # Writability check: current process must have write permission.
    mode = HOME.stat().st_mode
    assert bool(mode & stat.S_IWUSR), (
        "/home/user exists but is not writable; "
        "the student will be unable to create the required artefacts."
    )


def test_alerts_env_does_not_exist_yet():
    """
    The virtual-environment directory must NOT exist prior to the task.
    """
    _should_not_exist(ENV_DIR)


def test_alerts_env_bin_python_absent():
    """
    Bin/python inside the would-be venv must also not exist.
    """
    _should_not_exist(ENV_PYTHON)


def test_alerts_report_log_absent():
    """
    The report log must NOT exist before the student generates it.
    """
    _should_not_exist(REPORT_LOG)


def test_alerts_summary_txt_absent():
    """
    The summary file must NOT exist before the student creates it.
    """
    _should_not_exist(SUMMARY_TXT)