# test_initial_state.py
#
# This pytest suite verifies that the filesystem is in its **initial**
# state *before* the student performs any actions required by the
# “ping‐to‐localhost” task.
#
# The student will later have to:
#   1. Create /home/user/network_test
#   2. Inside it, create ping_result.log containing raw `ping` output
#
# Therefore, at this point in time **none** of these artefacts should
# exist.  If they do, the tests fail with an explicit explanation.

import os
import pytest
from pathlib import Path

BASE_DIR = Path("/home/user/network_test")
LOG_FILE = BASE_DIR / "ping_result.log"


def _pretty_permissions(path: Path) -> str:
    """
    Return a string representing the path’s permissions in octal form,
    e.g. '0o755', or '<missing>' if it does not exist.
    """
    if not path.exists():
        return "<missing>"
    return oct(path.stat().st_mode & 0o777)


@pytest.mark.describe("Initial filesystem state for ping connectivity task")
class TestInitialState:

    def test_network_test_directory_does_not_exist(self):
        """
        The target directory /home/user/network_test must NOT exist yet.
        Its presence would indicate that the setup work has already
        (incorrectly) been performed.
        """
        assert not BASE_DIR.exists(), (
            f"The directory {BASE_DIR} already exists with permissions "
            f"{_pretty_permissions(BASE_DIR)}. "
            "Start from a clean slate: remove or rename it before running the task."
        )

    def test_ping_result_log_does_not_exist(self):
        """
        The file /home/user/network_test/ping_result.log must NOT exist
        before the student runs the ping command and captures its output.
        """
        # If the directory itself is absent, the file is obviously absent,
        # but we still perform a direct check for completeness.
        assert not LOG_FILE.exists(), (
            f"The file {LOG_FILE} already exists. "
            "It should be created only after running a single-packet ping "
            "to 127.0.0.1 and capturing the raw console output."
        )

    def test_no_intermediate_parent_directories_exist(self):
        """
        None of the parent directories between /home/user and the target
        directory should pre-exist beyond the standard /home/user path.
        This guards against users accidentally creating nested directories
        such as /home/user/network_test/tmp or similar.
        """
        # Walk from /home/user up to but not including the base dir and
        # assert that no unexpected directories exist whose names start
        # with 'network_test'.
        home = Path("/home/user")
        for child in home.iterdir():
            if child.name.startswith("network_test"):
                pytest.fail(
                    f"Unexpected directory '{child}' found. Remove it so "
                    "the task starts from a pristine environment."
                )