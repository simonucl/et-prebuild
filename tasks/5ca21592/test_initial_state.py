# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem
# state **before** the student performs any actions for the “hello-time”
# exercise.  Nothing related to the task should exist yet.

import os
import stat
import pytest

HOME = "/home/user"
SCRIPTS_DIR = os.path.join(HOME, "scripts")
SCRIPT_FILE = os.path.join(SCRIPTS_DIR, "hello_time.sh")
SYSTEMD_SERVICE_FILE = os.path.join(
    HOME, ".config", "systemd", "user", "hello-time.service"
)
LOG_FILE = os.path.join(HOME, "hello_time.log")


def _human_readable_perm(mode: int) -> str:
    """Return a Unix-style rwx string for the owner bits only."""
    symbols = ["r", "w", "x"]
    owner_bits = (mode & 0o700) >> 6
    return "".join(symbols[i] if owner_bits & (1 << (2 - i)) else "-" for i in range(3))


@pytest.mark.parametrize(
    "path, what",
    [
        (SCRIPTS_DIR, "directory"),
        (SCRIPT_FILE, "script file"),
        (SYSTEMD_SERVICE_FILE, "systemd service unit"),
        (LOG_FILE, "log file"),
    ],
)
def test_artifacts_absent(path, what):
    """
    The student has not created any artifacts yet: the scripts directory,
    the shell script, the systemd unit and the log file must *not* exist
    at this stage.
    """
    assert not os.path.exists(
        path
    ), f"The {what} '{path}' should NOT exist before the task is started."


def test_no_executable_placeholder_script():
    """
    Guard against an empty placeholder script that is accidentally made
    executable.  If the script exists already we give a more specific
    error message so the student knows it must be removed before starting.
    """
    if os.path.exists(SCRIPT_FILE):
        st = os.stat(SCRIPT_FILE)
        owner_exec = bool(st.st_mode & stat.S_IXUSR)
        perms = _human_readable_perm(st.st_mode)
        pytest.fail(
            f"The script '{SCRIPT_FILE}' already exists with owner "
            f"permissions '{perms}' (executable={owner_exec}).  "
            "No script should be present yet."
        )