# test_initial_state.py
"""
Pytest suite that validates the *initial* operating-system / filesystem
state BEFORE the student performs the “SSH key-pair” task.

The tests purposefully:
    • Confirm that none of the artefacts the student is expected to create
      already exist.
    • Ensure we will not accidentally overwrite pre-existing content that
      already satisfies the final-state requirements (e.g. by containing
      the same comment).

All checks are performed against absolute paths under /home/user.
Only the Python standard library and pytest are used.
"""
import os
import stat
import shutil
from pathlib import Path

HOME = Path("/home/user")
SSH_DIR = HOME / ".ssh"
KEY_PRIVATE = SSH_DIR / "my_script_key"
KEY_PUBLIC = SSH_DIR / "my_script_key.pub"
AUTHORIZED_KEYS = SSH_DIR / "authorized_keys"
LOG_DIR = HOME / "ssh_setup"
LOG_FILE = LOG_DIR / "ssh_key_info.log"


def _human_mode(mode: int) -> str:
    """Return an octal string (e.g. '0o700') from st_mode."""
    return oct(mode & 0o777)


def test_ssh_keygen_available():
    """
    ssh-keygen must be present in PATH so the student can generate keys.
    """
    assert shutil.which("ssh-keygen") is not None, (
        "The `ssh-keygen` executable is not available in PATH. "
        "It is required for the upcoming exercise."
    )


def test_private_key_absent():
    """
    The new private key must *not* exist yet.
    """
    assert not KEY_PRIVATE.exists(), (
        f"Found unexpected private key at {KEY_PRIVATE}. "
        "The exercise requires the student to create this file."
    )


def test_public_key_absent():
    """
    The new public key must *not* exist yet.
    """
    assert not KEY_PUBLIC.exists(), (
        f"Found unexpected public key at {KEY_PUBLIC}. "
        "The exercise requires the student to create this file."
    )


def test_log_file_absent():
    """
    The log file should not exist prior to the exercise.
    """
    assert not LOG_FILE.exists(), (
        f"Found unexpected log file at {LOG_FILE}. "
        "The student must create it during the exercise."
    )


def test_authorized_keys_does_not_contain_new_entry():
    """
    If ~/.ssh/authorized_keys exists, it must NOT already contain a line
    ending with the comment 'script_dev@local'.  The student will append
    that line later.
    """
    if not AUTHORIZED_KEYS.exists():
        # Nothing to check if the file doesn't exist yet.
        return

    try:
        with AUTHORIZED_KEYS.open("r", encoding="utf-8") as fh:
            for ln_number, line in enumerate(fh, 1):
                if "script_dev@local" in line:
                    pytest_fail_msg = (
                        f"Line {ln_number} of {AUTHORIZED_KEYS} already "
                        "contains the comment 'script_dev@local'. "
                        "The student should add this line during the exercise, "
                        "so it must be absent at the initial state."
                    )
                    assert False, pytest_fail_msg
    except UnicodeDecodeError:
        assert False, (
            f"{AUTHORIZED_KEYS} exists but could not be read as UTF-8 text. "
            "Ensure it contains valid UTF-8 content."
        )


def test_ssh_directory_permissions_are_sane():
    """
    If ~/.ssh exists, its permissions should be reasonably restrictive
    (not world-writable).  This is a *sanity* check; it does not enforce the
    final required mode of 0700 because that will be set later.
    """
    if not SSH_DIR.exists():
        # Directory does not exist yet, which is fine at initial state.
        return

    mode = SSH_DIR.stat().st_mode
    world_write = bool(mode & stat.S_IWOTH)
    assert not world_write, (
        f"{SSH_DIR} is world-writable (mode {_human_mode(mode)}). "
        "It should not be world-writable; please fix before proceeding."
    )