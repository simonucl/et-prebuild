# test_initial_state.py
#
# This pytest suite validates the *initial* operating–system / filesystem
# state before the student starts working on the “security-oriented log
# analyst” task.  It deliberately avoids looking for (or at) any of the
# files / directories that the student is expected to create later on.
#
# The checks below make sure that
#
#   1. A valid home directory (/home/user) is present and writable.
#   2. The OpenSSH “ssh-keygen” utility required for key creation is
#      available and actually able to create a throw-away key in a
#      temporary directory.
#
# Only standard-library modules plus pytest are used.

import os
import shutil
import stat
import subprocess
from pathlib import Path

import pytest


HOME_DIR = Path("/home/user")


def test_home_directory_exists_and_writable():
    """
    The exercise assumes the account 'user' has a proper, writable home
    directory.  Verify it exists and basic permissions allow writing.
    """
    assert HOME_DIR.exists(), f"Expected home directory {HOME_DIR} is missing."
    assert HOME_DIR.is_dir(), f"{HOME_DIR} exists but is not a directory."
    assert os.access(HOME_DIR, os.W_OK), (
        f"Home directory {HOME_DIR} is not writable for the current user."
    )


def test_ssh_keygen_is_available():
    """
    'ssh-keygen' must be in $PATH so the student can generate SSH keys.
    """
    ssh_keygen_path = shutil.which("ssh-keygen")
    assert (
        ssh_keygen_path is not None
    ), "'ssh-keygen' executable not found in PATH. It is required for the exercise."
    # Quick sanity check: the binary found must be executable.
    assert os.access(
        ssh_keygen_path, os.X_OK
    ), f"Found ssh-keygen at {ssh_keygen_path}, but it is not executable."


def test_ssh_keygen_can_create_a_key(tmp_path):
    """
    Beyond mere presence, ensure ssh-keygen can successfully generate
    an RSA key in a throw-away directory.  This guards against broken
    installations or missing crypto libraries.
    """
    # Paths for a temporary, disposable key pair.
    private_key = tmp_path / "probe_key"
    public_key = tmp_path / "probe_key.pub"

    # Build the ssh-keygen command.
    cmd = [
        "ssh-keygen",
        "-t",
        "rsa",
        "-b",
        "1024",  # smaller key for speed; just a functionality probe
        "-N",
        "",  # no passphrase
        "-C",
        "",  # empty comment
        "-f",
        str(private_key),
        "-q",  # quiet
    ]

    # Run ssh-keygen.
    completed = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    assert (
        completed.returncode == 0
    ), f"'ssh-keygen' failed to generate a test key.\nSTDOUT: {completed.stdout.decode()}\nSTDERR: {completed.stderr.decode()}"

    # Confirm the expected files exist.
    assert private_key.exists(), "ssh-keygen did not create the private key file."
    assert public_key.exists(), "ssh-keygen did not create the public key file."

    # Verify minimal permission sanity on the private key (should not be world-readable).
    private_mode = stat.S_IMODE(private_key.stat().st_mode)
    assert (
        private_mode & 0o077 == 0
    ), f"Temporary private key has overly permissive mode {oct(private_mode)}. ssh-keygen might be mis-configured."

    # No explicit cleanup needed; pytest will remove tmp_path automatically.