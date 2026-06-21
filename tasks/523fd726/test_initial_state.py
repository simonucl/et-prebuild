# test_initial_state.py
#
# This test-suite verifies that the filesystem is in a **clean, pre-provisioning
# state**.  None of the artefacts that the student is expected to create should
# be present yet.  If any of them already exist, the environment is considered
# tainted and the test will fail with a clear, actionable message.
#
# Checked paths (MUST be absent before the student starts):
#   1. /home/user/.config/exampled/cache-clean.conf
#   2. /home/user/.config/exampled/           (directory)
#   3. /home/user/logs/provisioning_steps.log
#   4. /home/user/logs/                       (directory)
#
# Only the Python standard library and pytest are used.

import os
import stat
import pytest

HOME = "/home/user"
CONFIG_DIR = os.path.join(HOME, ".config", "exampled")
CONFIG_FILE = os.path.join(CONFIG_DIR, "cache-clean.conf")
LOG_DIR = os.path.join(HOME, "logs")
LOG_FILE = os.path.join(LOG_DIR, "provisioning_steps.log")


@pytest.mark.describe("Pre-provisioning filesystem state")
class TestInitialState:
    def _assert_not_exists(self, path, what):
        """
        Helper: assert that `path` does *not* exist.  If it does, fail with an
        informative message so that the student (or the CI provider) knows
        exactly what needs to be cleaned up.
        """
        assert not os.path.exists(path), (
            f"{what} already exists at {path!r}. "
            "The environment must start clean; remove it before running the "
            "provisioning script."
        )

    def test_config_file_absent(self):
        """The configuration file must NOT yet exist."""
        self._assert_not_exists(CONFIG_FILE, "Configuration file")

    def test_config_dir_absent(self):
        """
        The configuration directory must NOT exist.  If the directory is
        already present, the student would not be responsible for creating it.
        """
        self._assert_not_exists(CONFIG_DIR, "Configuration directory")

    def test_log_file_absent(self):
        """The provisioning log file must NOT yet exist."""
        self._assert_not_exists(LOG_FILE, "Provisioning log file")

    def test_log_dir_absent(self):
        """
        The logs directory must NOT exist.  Its creation is part of the task
        specification.
        """
        self._assert_not_exists(LOG_DIR, "Logs directory")