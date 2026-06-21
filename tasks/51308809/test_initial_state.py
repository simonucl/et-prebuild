# test_initial_state.py
#
# This pytest suite validates that the operating-system / file-system is
# in the correct “initial” state *before* the student performs any actions
# for the “backup engineer” assignment.
#
# The checks intentionally avoid touching any of the artefacts that the
# student is supposed to create (keys/, key-files, log-file, …).  We only
# verify items that must already be present.

import os
import stat
from pathlib import Path

import pytest

HOME = Path("/home/user")

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def is_writable(path: Path) -> bool:
    """
    Returns True if the current user can create files inside ``path``.
    """
    return os.access(path, os.W_OK)


# ---------------------------------------------------------------------------
# Tests for the pre-existing environment
# ---------------------------------------------------------------------------

def test_backup_verification_directory_exists_and_is_writable():
    """
    The directory /home/user/backup_verification must already exist and be
    writable by the student.  (Sub-directories and files inside it will be
    created later and are *not* checked here.)
    """
    dir_path = HOME / "backup_verification"

    assert dir_path.exists(), (
        f"Expected directory {dir_path} to exist but it is missing.  "
        "This directory must be present *before* the student starts."
    )
    assert dir_path.is_dir(), (
        f"{dir_path} exists but is not a directory.  "
        "Please ensure it is an actual directory."
    )
    assert is_writable(dir_path), (
        f"Directory {dir_path} is not writable by the current user.  "
        "The student will need write access to create keys and logs."
    )


def test_remote_authorized_keys_exists_and_is_clean():
    """
    The simulated remote host’s authorized_keys file must already exist
    and contain only the single comment line provided by the starter
    repository.  No public-key lines should be present yet.
    """
    ak_path = HOME / "remote_host" / ".ssh" / "authorized_keys"

    assert ak_path.exists(), (
        f"Expected file {ak_path} to exist but it is missing.  "
        "The exercise description states that a comment line must already "
        "be present."
    )
    assert ak_path.is_file(), (
        f"{ak_path} exists but is not a regular file."
    )

    # Read file contents
    with ak_path.open("r", encoding="utf-8") as fh:
        lines = [ln.rstrip("\n") for ln in fh]

    # There must be at least one line (the starter comment).
    assert lines, (
        f"{ak_path} is empty.  It should at minimum contain the comment line "
        "'# remote host authorized keys'."
    )

    # The very first non-blank line must be the expected comment.
    non_blank = next((ln for ln in lines if ln.strip()), "")
    expected_comment = "# remote host authorized keys"
    assert non_blank == expected_comment, (
        f"The first non-blank line of {ak_path} must be exactly:\n"
        f"    {expected_comment!r}\n"
        f"but found:\n"
        f"    {non_blank!r}"
    )

    # There must not yet be any public keys in the file.
    disallowed_prefixes = ("ssh-rsa ", "ssh-ed25519 ", "ecdsa-sha2", "sk-")
    key_lines = [
        ln for ln in lines
        if any(ln.strip().startswith(prefix) for prefix in disallowed_prefixes)
    ]
    assert not key_lines, (
        f"{ak_path} already contains SSH public keys:\n"
        + "\n".join(f"    {ln}" for ln in key_lines) + "\n"
        "It should only have the comment line at this stage."
    )


def test_remote_host_ssh_directory_permissions_sane():
    """
    Verify that /home/user/remote_host/.ssh is a directory with permissions
    that do not expose private data (i.e. not world-writable).
    """
    ssh_dir = HOME / "remote_host" / ".ssh"
    assert ssh_dir.exists(), (
        f"Directory {ssh_dir} does not exist.  "
        "It should have been created in the starter environment."
    )
    assert ssh_dir.is_dir(), f"{ssh_dir} exists but is not a directory."

    mode = ssh_dir.stat().st_mode
    world_writable = bool(mode & stat.S_IWOTH)
    assert not world_writable, (
        f"Directory {ssh_dir} is world-writable, which is insecure.  "
        "Permissions should not allow global write access."
    )