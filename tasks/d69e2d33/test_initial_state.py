# test_initial_state.py
#
# This test-suite validates that the operating-system / filesystem
# is in the *expected* pristine state **before** the student starts
# the exercise.  The task instructions explicitly say that neither
# the directory `/home/user/logs` nor the file
# `/home/user/logs/loopback_ping.log` should exist yet; the student
# will create them later.  If either one is already present, we fail
# early with a clear, actionable message so the learner knows the
# environment is not clean.

import os
from pathlib import Path
import pytest

HOME_DIR = Path("/home/user")
LOG_DIR = HOME_DIR / "logs"
LOG_FILE = LOG_DIR / "loopback_ping.log"


def _human(path: Path) -> str:
    """Return a human-readable path description for error messages."""
    return f"‘{str(path)}’"


@pytest.mark.describe("Initial OS / filesystem state")
class TestInitialState:

    def test_log_directory_does_not_exist(self):
        """
        The directory /home/user/logs must NOT exist before the task begins.
        """
        assert not LOG_DIR.exists(), (
            f"The directory {_human(LOG_DIR)} already exists, but the task "
            f"requires starting with a clean slate. Remove it before proceeding."
        )

    def test_log_file_does_not_exist(self):
        """
        The file /home/user/logs/loopback_ping.log must NOT exist before the task begins.
        """
        assert not LOG_FILE.exists(), (
            f"The file {_human(LOG_FILE)} already exists, which indicates the "
            f"diagnostic log has been created prematurely. Start from a fresh "
            f"environment with no such file."
        )

    def test_no_parent_logs_in_home(self):
        """
        Sanity-check: there should be no lingering 'logs' directories at any other depth
        under /home/user that could confuse the student.
        """
        stray_logs = [p for p in HOME_DIR.rglob("logs") if p.is_dir()]
        assert not stray_logs, (
            "Found unexpected 'logs' directories in the workspace:\n" +
            "\n".join(str(p) for p in stray_logs) +
            "\nRemove or rename them to ensure a clean starting point."
        )