# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem
# state **before** the student starts working on the “fresh deploy key”
# exercise.  These checks guarantee that the required prerequisites are in
# place and that nothing already violates the assumptions described in the
# task text.

import os
import stat
import shutil
from pathlib import Path

import pytest

HOME = Path("/home/user")
SSH_DIR = HOME / ".ssh"
AUTH_KEYS = SSH_DIR / "authorized_keys"
EXPECTED_OLD_KEY = (
    "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIB3j6Lm9vDGf/oldexamplekey== dev@old"
)


def _is_writable_directory(path: Path) -> bool:
    """
    Return True if *path* exists, is a directory and is user-writable.
    This helper keeps the individual tests readable.
    """
    return path.is_dir() and os.access(str(path), os.W_OK | os.X_OK)


def test_ssh_directory_exists_and_is_writable():
    """
    The directory /home/user/.ssh must already exist and be writable so that the
    student can create keys and the authorized_keys file inside it.
    """
    assert SSH_DIR.exists(), (
        f"The directory {SSH_DIR} does not exist. "
        "Create it with `mkdir -p ~/.ssh` before generating keys."
    )
    assert SSH_DIR.is_dir(), f"{SSH_DIR} exists but is not a directory."

    assert _is_writable_directory(
        SSH_DIR
    ), f"{SSH_DIR} is not writable to the current user."


def test_authorized_keys_initial_contents():
    """
    authorised_keys may or may not pre-exist.  If it exists it must contain
    exactly the single, pre-defined ed25519 key and nothing else.  This ensures
    the checker can unambiguously verify that the student appends *one* new key
    without altering the old one.
    """
    if not AUTH_KEYS.exists():
        # File is optional at the start; absence is perfectly fine.
        pytest.skip(f"{AUTH_KEYS} does not exist yet — that is acceptable.")
        return

    # File exists – verify readability and contents.
    assert AUTH_KEYS.is_file(), f"{AUTH_KEYS} exists but is not a regular file."
    assert os.access(str(AUTH_KEYS), os.R_OK | os.W_OK), (
        f"{AUTH_KEYS} is not readable/writable by the current user. "
        "Adjust the permissions so that new keys can be appended."
    )

    with AUTH_KEYS.open("r", encoding="utf-8") as fh:
        lines = [ln.rstrip("\n") for ln in fh.readlines()]

    # Ignore empty trailing lines (some editors leave a blank newline)
    non_blank_lines = [ln for ln in lines if ln.strip()]

    assert non_blank_lines == [
        EXPECTED_OLD_KEY
    ], (
        f"{AUTH_KEYS} should contain exactly one key line:\n"
        f"  {EXPECTED_OLD_KEY}\n"
        "Either the file has been modified already or contains unexpected data."
    )


def test_ssh_keygen_available():
    """
    The exercise requires ssh-keygen.  Verify that the binary is available in
    $PATH so the student can execute it.
    """
    assert (
        shutil.which("ssh-keygen") is not None
    ), "The `ssh-keygen` executable is not found in PATH."