# test_initial_state.py
#
# Pytest suite that verifies the machine is in the **initial** state
# before the student creates `/home/user/network_diagnostic.log`.
#
# Expectations for the pristine environment:
#   1. The home directory `/home/user` exists.
#   2. The target artefact `/home/user/network_diagnostic.log` **does not** exist yet.
#   3. The commands required for the task (`ip`, `ss`, `ping`) are present
#      somewhere in the current `$PATH`.
#
# If any of these pre-conditions fail, the tests will emit clear,
# actionable error messages.

import os
import shutil
import stat
import pytest

HOME_DIR = "/home/user"
LOG_PATH = "/home/user/network_diagnostic.log"
REQUIRED_CMDS = ("ip", "ss", "ping")


def _perm_str(mode: int) -> str:
    """
    Helper to render a Unix permission integer (e.g., 0o644) as a
    human-readable string ('-rw-r--r--') for clearer failure messages.
    """
    is_dir = "d" if stat.S_ISDIR(mode) else "-"
    perms = ""
    for who in (stat.S_IRUSR, stat.S_IWUSR, stat.S_IXUSR,
                stat.S_IRGRP, stat.S_IWGRP, stat.S_IXGRP,
                stat.S_IROTH, stat.S_IWOTH, stat.S_IXOTH):
        perms += (mode & who) and "rwxrwxrwx"[ (who.bit_length() - 1) % 9 ] or "-"
    return is_dir + perms


def test_home_directory_exists():
    assert os.path.isdir(HOME_DIR), (
        f"Expected home directory '{HOME_DIR}' to exist, "
        "but it is missing or not a directory."
    )


def test_artifact_does_not_exist_yet():
    assert not os.path.exists(LOG_PATH), (
        f"Found '{LOG_PATH}', but the diagnostic report must **not** "
        "exist before the student runs their solution."
    )


@pytest.mark.parametrize("cmd", REQUIRED_CMDS)
def test_required_commands_available(cmd):
    path = shutil.which(cmd)
    assert path, (
        f"Required command '{cmd}' not found in $PATH. "
        "Ensure the base image includes this binary."
    )