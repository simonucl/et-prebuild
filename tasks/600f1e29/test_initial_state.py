# test_initial_state.py
#
# This pytest suite validates the *initial* state of the operating-system
# and filesystem **before** the student performs any actions required by
# the “disk-usage audit trail” task.  Nothing created by the task should
# exist yet.

import os
import stat
import shutil
import subprocess
import pytest
from pathlib import Path

HOME = Path("/home/user")
AUDIT_DIR = HOME / "audit_trails"
AUDIT_LOG = AUDIT_DIR / "disk_usage_audit.log"


def _check_command_available(cmd: str) -> None:
    """
    Helper that asserts a given GNU/Linux user-level command is available
    on the PATH and is executable.  We use shutil.which instead of trying
    to run the command because that relies only on the stdlib.
    """
    cmd_path = shutil.which(cmd)
    assert (
        cmd_path is not None
    ), f"The command '{cmd}' is required for this exercise but is not found on PATH."
    assert os.access(
        cmd_path, os.X_OK
    ), f"The command '{cmd}' at '{cmd_path}' exists but is not executable."


@pytest.mark.describe("Baseline operating system checks")
class TestInitialState:
    def test_home_directory_exists_and_is_dir(self):
        assert HOME.exists(), "Expected /home/user to exist, but it is missing."
        assert HOME.is_dir(), "/home/user exists but is not a directory."

    @pytest.mark.parametrize("cmd", ["df", "du", "head"])
    def test_required_commands_available(self, cmd):
        _check_command_available(cmd)

    def test_audit_directory_does_not_exist_yet(self):
        """
        The audit_trails directory must NOT exist before the student
        creates it.
        """
        assert not AUDIT_DIR.exists(), (
            f"The directory '{AUDIT_DIR}' already exists. "
            "It should be created by the student during the task."
        )

    def test_audit_log_file_does_not_exist_yet(self):
        """
        The audit log file must NOT exist before the student runs the
        required commands.
        """
        assert not AUDIT_LOG.exists(), (
            f"The file '{AUDIT_LOG}' already exists. "
            "It should be created by the student during the task."
        )

    def test_no_partial_audit_files_present(self):
        """
        Ensure no files that could be mistaken for the target audit log
        are already present inside /home/user.
        """
        offenders = []
        for path in HOME.rglob("*audit*.log"):
            offenders.append(str(path))
        assert (
            not offenders
        ), f"Found pre-existing audit-related log files that should not exist yet: {offenders}"