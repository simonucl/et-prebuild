# test_initial_state.py
#
# Pytest suite that verifies the machine is in a clean state
# BEFORE the student performs the “dummy restore” drill.
#
# These tests intentionally fail if:
#   •  /home/user/restore_test/restore_session.log already exists.
#   •  A background process that looks like the dummy “sleep 120”
#      job is already running for the current user.
#
# Nothing in these tests checks for the final artefacts––they only make
# sure the starting point is sane.

import os
import pwd
import subprocess
import shlex
import sys
import pytest

LOG_DIR = "/home/user/restore_test"
LOG_FILE = os.path.join(LOG_DIR, "restore_session.log")


def _sleep_120_processes():
    """
    Return a list of (pid, cmdline) tuples for processes owned by the current
    user whose *entire* command-line is exactly 'sleep 120'.
    """
    username = pwd.getpwuid(os.getuid()).pw_name

    # The output format without headers:
    #   <pid> <full command line>
    ps_cmd = ["ps", "-u", username, "-o", "pid=", "-o", "args="]
    try:
        out = subprocess.check_output(ps_cmd, text=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as exc:
        pytest.fail(f"Could not run {' '.join(ps_cmd)}:\n{exc.output}")

    offenders = []
    for line in out.strip().splitlines():
        line = line.rstrip()
        if not line:
            continue
        # Split only once: pid   rest_of_line
        pid_str, _, cmd = line.partition(" ")
        pid_str = pid_str.strip()
        cmd = cmd.strip()
        if cmd == "sleep 120":
            offenders.append((pid_str, cmd))
    return offenders


def test_restore_log_file_absent():
    """
    The audit log must NOT exist before the student starts the exercise.
    """
    assert not os.path.exists(LOG_FILE), (
        f"Pre-condition failed: {LOG_FILE} already exists. "
        "The exercise requires you to create it during the drill, "
        "but it is present beforehand."
    )


def test_preexisting_sleep_120_processes():
    """
    No leftover 'sleep 120' processes should be running for the current user.
    """
    offenders = _sleep_120_processes()
    assert not offenders, (
        "Pre-condition failed: found an existing dummy 'sleep 120' process:\n"
        + "\n".join(f"PID {pid}: {cmd}" for pid, cmd in offenders)
        + "\nPlease make sure no prior test restore job is still running."
    )


def test_log_directory_state():
    """
    The directory may or may not exist, but if it does, it should be clean:
    no restore_session.log should be present yet.
    """
    if os.path.exists(LOG_DIR):
        assert os.path.isdir(LOG_DIR), (
            f"Expected {LOG_DIR} to be a directory, but it is not."
        )
        assert not os.path.exists(LOG_FILE), (
            f"Found {LOG_FILE} in an existing directory. "
            "The file must be created during the exercise, not before."
        )