# test_initial_state.py
#
# This test-suite validates the *initial* filesystem state **before**
# the student creates any files for the “systemd user timer” task.
#
# Expectations:
# 1. The student’s home directory exists (/home/user).
# 2. None of the target artefacts have been created yet:
#    • /home/user/.config/systemd/user/hello-date.service
#    • /home/user/.config/systemd/user/hello-date.timer
#    • /home/user/task_verification/created_files.log
#
# If any of the above artefacts already exist, the subsequent grading
# could give a false positive, so we fail early with an informative
# message.

import os
import pytest

HOME = "/home/user"
SERVICE_PATH = os.path.join(
    HOME, ".config", "systemd", "user", "hello-date.service"
)
TIMER_PATH = os.path.join(
    HOME, ".config", "systemd", "user", "hello-date.timer"
)
VERIFICATION_LOG = os.path.join(
    HOME, "task_verification", "created_files.log"
)


@pytest.fixture(scope="module")
def home_dir():
    """Return /home/user; fail if it is missing or not a directory."""
    assert os.path.isdir(HOME), (
        f"Expected user home directory at {HOME!r}, "
        "but it does not exist or is not a directory."
    )
    return HOME


def _assert_absent(path: str):
    """Helper: assert that *path* is absent (does not exist)."""
    assert not os.path.exists(
        path
    ), f"Pre-condition failed: {path!r} already exists but should not."


def test_service_file_absent_before_start(home_dir):
    _assert_absent(SERVICE_PATH)


def test_timer_file_absent_before_start(home_dir):
    _assert_absent(TIMER_PATH)


def test_verification_log_absent_before_start(home_dir):
    _assert_absent(VERIFICATION_LOG)