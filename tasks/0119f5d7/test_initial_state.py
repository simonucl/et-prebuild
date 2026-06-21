# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem
# state before the student carries out the “uptime-monitor” SSH-key task.
#
# These tests purposefully assert that the target objects (directory, keys,
# log file) do **NOT** exist yet.  A failure here means the sandbox is in an
# unexpected state *before* the student starts, which would make the real
# evaluation unreliable.

import os
import shutil
from pathlib import Path

HOME = Path("/home/user")
SSH_DIR = HOME / ".ssh"
UPTIME_DIR = SSH_DIR / "uptime_monitor"
PRIV_KEY = UPTIME_DIR / "id_ed25519"
PUB_KEY = UPTIME_DIR / "id_ed25519.pub"
LOG_FILE = HOME / "uptime_key_info.log"


def test_home_directory_exists():
    assert HOME.is_dir(), (
        f"Expected home directory {HOME} to exist in the sandbox, "
        "but it does not.  Nothing else can be tested without it."
    )


def test_target_directory_absent():
    assert not UPTIME_DIR.exists(), (
        f"Directory {UPTIME_DIR} already exists.  The task requires the "
        "student to create it, so the starting environment must *not* "
        "contain it."
    )


def test_key_files_absent():
    for key_path in (PRIV_KEY, PUB_KEY):
        assert not key_path.exists(), (
            f"Key file {key_path} already exists.  The student must generate "
            "this key during the exercise, so the file should not be present "
            "at the outset."
        )


def test_log_file_absent():
    assert not LOG_FILE.exists(), (
        f"Log file {LOG_FILE} already exists.  The student must create it "
        "as part of the assignment, so it should not be present beforehand."
    )


def test_ssh_keygen_available():
    """
    A functional ssh-keygen binary is required for the student to
    complete the exercise.  Make sure it is in PATH.
    """
    keygen_path = shutil.which("ssh-keygen")
    assert keygen_path, (
        "The `ssh-keygen` utility is not available in PATH.  The student "
        "cannot generate SSH keys without it."
    )
    # Extra sanity check: binary should be executable
    assert os.access(keygen_path, os.X_OK), (
        f"`ssh-keygen` found at {keygen_path}, but it is not executable."
    )