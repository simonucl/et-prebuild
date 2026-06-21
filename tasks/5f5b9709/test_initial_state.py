# test_initial_state.py
#
# This test-suite validates the *initial* state of the operating-system /
# filesystem **before** the student carries out the assignment.  Nothing related
# to the required deliverable should be present yet.
#
# Rules verified here:
#   1. The parent directory /home/user/build_net_diag/ must **not** exist.
#   2. Consequently, the sub-directory “…/logs/” must not exist either.
#   3. The target log file “…/logs/network_diagnostic.log” must not exist.
#
# If any of these items are already on disk the assignment clearly has been
# (partially) executed and the initial-state check must fail with a clear
# message so the learner knows to start from a clean environment.

import os
import pytest
from pathlib import Path

BASE_DIR = Path("/home/user/build_net_diag")
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "network_diagnostic.log"


def _human(path: Path) -> str:
    """Return a quoted, human-friendly string for error messages."""
    return f"'{path.as_posix()}'"


@pytest.mark.describe("Initial filesystem sanity checks")
class TestInitialState:
    def test_base_directory_absent(self):
        """The top-level directory may not exist yet."""
        assert not BASE_DIR.exists(), (
            f"The directory {_human(BASE_DIR)} already exists, "
            "but it should NOT be present before you start the task."
        )

    def test_logs_directory_absent(self):
        """The logs/ directory must not exist yet."""
        assert not LOG_DIR.exists(), (
            f"The directory {_human(LOG_DIR)} already exists, "
            "but it should NOT exist in the initial state."
        )

    def test_log_file_absent(self):
        """The target log file must not exist yet."""
        assert not LOG_FILE.exists(), (
            f"The file {_human(LOG_FILE)} already exists, "
            "but it should NOT be present before the diagnostic script runs."
        )