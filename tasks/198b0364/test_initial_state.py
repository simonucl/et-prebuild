# test_initial_state.py
#
# This test-suite is executed **before** the student has run any commands.
# It ensures that the workspace is clean and that none of the artefacts the
# student is asked to create are already present.  If any of these files
# already exist, the exercise would be meaningless (or the student would be
# unintentionally helped), so we fail fast with an explanatory message.

import os
from pathlib import Path
import stat
import pytest

HOME = Path("/home/user")
SSH_DIR = HOME / ".ssh"

PRIV_KEY = SSH_DIR / "network_lab_key"
PUB_KEY = SSH_DIR / "network_lab_key.pub"
AUTH_KEYS = SSH_DIR / "authorized_keys"
LOG_FILE = HOME / "ssh_setup.log"


def _human_readable_mode(path: Path) -> str:
    """
    Return the file's permission bits in octal (e.g. '0o600') or
    'N/A' if the file does not exist (used solely for error messages).
    """
    try:
        mode = oct(path.stat().st_mode & 0o777)
    except FileNotFoundError:
        mode = "N/A"
    return mode


@pytest.mark.parametrize(
    "p, desc",
    [
        (PRIV_KEY, "private key"),
        (PUB_KEY, "public key"),
    ],
)
def test_key_files_do_not_yet_exist(p: Path, desc: str):
    """
    The ED25519 key-pair must not exist prior to the student's work.
    """
    assert not p.exists(), (
        f"The {desc} '{p}' already exists.\n"
        "The exercise requires the student to generate this file from scratch, "
        "so it must be absent at the start."
    )


def test_log_file_does_not_yet_exist():
    """
    The setup log must not pre-exist.
    """
    assert not LOG_FILE.exists(), (
        f"The log file '{LOG_FILE}' is already present.\n"
        "It should be created by the student's script, not shipped with the "
        "initial environment."
    )


def test_authorized_keys_is_safe_to_overwrite():
    """
    The student is instructed to create (or truncate) authorized_keys so that
    it contains exactly ONE line: the freshly generated public key.

    We therefore allow for two valid initial states:
      1. The file is absent (most common).
      2. The file exists but is NOT write-protected; i.e. the user can safely
         truncate it.

    Any other situation (e.g. a directory in its place, or a read-only file)
    would block the student and should be flagged.
    """
    if not AUTH_KEYS.exists():
        # Nothing to verify if the file is absent.
        return

    # It exists — ensure it is a regular file and writable.
    assert AUTH_KEYS.is_file(), (
        f"'{AUTH_KEYS}' exists but is not a regular file; "
        "the student would be unable to replace/truncate it."
    )

    # Test writability with the current user's permissions
    writable = os.access(AUTH_KEYS, os.W_OK)
    assert writable, (
        f"'{AUTH_KEYS}' is present but NOT writable "
        f"(mode is {_human_readable_mode(AUTH_KEYS)}). "
        "The student needs to truncate this file."
    )


def test_ssh_directory_state_is_reasonable():
    """
    The ~/.ssh directory may or may not exist beforehand.  If it *does* exist,
    we check that it is in fact a directory and that the current user can
    create new files inside it.
    """
    if not SSH_DIR.exists():
        # No directory yet — perfectly acceptable.
        return

    assert SSH_DIR.is_dir(), (
        f"'{SSH_DIR}' exists but is not a directory. "
        "This would prevent the student from creating SSH keys."
    )

    creatable = os.access(SSH_DIR, os.W_OK | os.X_OK)
    assert creatable, (
        f"'{SSH_DIR}' exists but the user lacks write/execute permissions "
        f"(mode is {_human_readable_mode(SSH_DIR)}). "
        "The student must be able to create files inside this directory."
    )