# test_initial_state.py
#
# Pytest suite that validates the machine _before_ the learner begins the task
# of installing “loguru==0.7.0” and writing the required report file.
#
# Expectations for the pristine state:
#   1. /home/user/log_install_report.txt must NOT exist yet.
#   2. The Python package “loguru” must either be completely absent or, if it
#      does exist, it must NOT be exactly version 0.7.0.  (Any other version
#      is considered “not yet done” because the learner still has to install
#      the requested one.)
#
# If any of these checks fail, the learner has somehow already done (part of)
# the graded task or the test environment is polluted, so the test will raise
# a clear assertion failure explaining what is wrong.
#
# Standard library only + pytest.

import os
import importlib
import importlib.util
import pytest

REPORT_PATH = "/home/user/log_install_report.txt"
TARGET_VERSION = "0.7.0"


def test_report_file_does_not_exist():
    """
    The report file should not be present before the student runs the required
    commands.  Its existence would mean the task has (at least partially)
    already been completed.
    """
    assert not os.path.exists(
        REPORT_PATH
    ), (
        f"The report file {REPORT_PATH!r} already exists. "
        "The environment is not in its initial state."
    )


def test_loguru_not_already_installed_at_target_version():
    """
    Either 'loguru' is not installed at all, or—if installed—must not yet be
    at the exact version the assignment asks for (0.7.0).  Having the correct
    version already present would defeat the purpose of the exercise.
    """
    spec = importlib.util.find_spec("loguru")

    # Package completely absent: that's fine for the initial state.
    if spec is None:
        pytest.skip("Package 'loguru' not present: clean initial state confirmed.")

    # Package present: verify it's NOT the target version.
    loguru = importlib.import_module("loguru")
    current_version = getattr(loguru, "__version__", "unknown")

    assert (
        current_version != TARGET_VERSION
    ), (
        "Package 'loguru' is already installed at version "
        f"{TARGET_VERSION}, but it should not be present (or should be at a "
        "different version) before the learner performs the task."
    )