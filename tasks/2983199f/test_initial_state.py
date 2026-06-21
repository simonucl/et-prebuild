# test_initial_state.py
#
# Pytest suite ensuring the operating-system / filesystem is clean
# BEFORE the student rotates the SSH key-material.
#
# The student’s single-command solution is expected to create:
#   1) /home/user/.ssh/policy_ed25519          (private key, mode 600)
#   2) /home/user/.ssh/policy_ed25519.pub      (public key, comment “policy-enforced-2023”)
#   3) /home/user/policy_key_creation.log      (3-line audit log)
#
# Therefore, none of those artefacts may exist at the outset.

import os
import stat
from pathlib import Path
import pytest


# Constants for full paths
HOME = Path("/home/user")
SSH_DIR = HOME / ".ssh"
PRIV_KEY = SSH_DIR / "policy_ed25519"
PUB_KEY = SSH_DIR / "policy_ed25519.pub"
AUDIT_LOG = HOME / "policy_key_creation.log"


@pytest.mark.parametrize(
    "path_obj, description",
    [
        (PRIV_KEY, "private key"),
        (PUB_KEY, "public key"),
        (AUDIT_LOG, "audit log"),
    ],
)
def test_no_preexisting_files(path_obj: Path, description: str):
    """
    None of the target artefacts should exist prior to running the student’s command.
    """
    assert not path_obj.exists(), (
        f"The {description} '{path_obj}' already exists. "
        "The environment must be clean before the key-rotation task begins."
    )


def test_ssh_directory_is_not_world_writable():
    """
    The ~/.ssh directory itself should never be world-writable; this check prevents
    accidental insecure test environments while still allowing the directory to be
    absent (the student may create it).
    """
    if not SSH_DIR.exists():
        pytest.skip("~/.ssh directory does not exist yet; this is acceptable.")
    mode = SSH_DIR.stat().st_mode
    world_write = bool(mode & stat.S_IWOTH)
    assert not world_write, (
        f"The directory '{SSH_DIR}' is world-writable, which is insecure. "
        "Please fix directory permissions before proceeding."
    )