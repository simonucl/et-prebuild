# test_initial_state.py
#
# Pytest suite that verifies the *initial* state of the filesystem
# before the student generates the diagnostics report.
#
# The assignment requires the learner to create:
#   /home/user/diagnostics/summary.log
#
# Therefore, *prior* to running the learner’s solution, neither the
# diagnostics directory nor the summary.log file should exist.
#
# Only standard‐library modules + pytest are used.

import os
import stat
import pytest

HOME_DIR = "/home/user"
DIAG_DIR = os.path.join(HOME_DIR, "diagnostics")
REPORT_FILE = os.path.join(DIAG_DIR, "summary.log")


def _path_state(path):
    """
    Helper that returns a string describing how a path exists, for
    better assertion error messages.
    """
    if not os.path.exists(path):
        return "does not exist"
    if os.path.isdir(path):
        return "is a directory"
    if os.path.isfile(path):
        return "is a file"
    # Could be symlink, socket, etc.; describe generically.
    mode = os.stat(path).st_mode
    kind = stat.S_IFMT(mode)
    return f"exists with mode {oct(kind)}"


@pytest.mark.order(1)
def test_home_directory_exists():
    """Ensure the base /home/user directory is present."""
    assert os.path.isdir(HOME_DIR), (
        f"Expected the home directory {HOME_DIR} to exist "
        f"and be a directory, but it {_path_state(HOME_DIR)}."
    )


@pytest.mark.order(2)
def test_diagnostics_directory_absent():
    """
    The diagnostics directory should NOT exist yet.
    It will be created by the student's submission.
    """
    assert not os.path.exists(DIAG_DIR), (
        "The diagnostics directory should not exist before the student runs "
        f"their solution, but {DIAG_DIR} {_path_state(DIAG_DIR)}."
    )


@pytest.mark.order(3)
def test_summary_log_absent():
    """
    The summary log must not exist prior to execution of the student's script.
    """
    assert not os.path.exists(REPORT_FILE), (
        "The diagnostics summary file should not be present yet. "
        f"Found that {REPORT_FILE} {_path_state(REPORT_FILE)}."
    )