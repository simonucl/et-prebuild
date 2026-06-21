# test_initial_state.py
#
# Pytest suite that validates the operating-system state *before* the student
# performs any actions.  It confirms that the provided OpenSSH sample
# configuration file exists (and is untouched) while deliberately *not* looking
# for any of the files/directories the student is expected to create later.
#
# Only the Python standard library and pytest are used.

import os
import stat
from pathlib import Path

import pytest


# Constants for paths we expect to exist right now
SAMPLE_DIR = Path("/home/user/sample_configs")
SAMPLE_FILE = SAMPLE_DIR / "sshd_config"


def test_sample_directory_exists():
    """
    The directory /home/user/sample_configs must already exist and be a directory.
    """
    assert SAMPLE_DIR.exists(), (
        f"Required directory {SAMPLE_DIR} is missing. "
        "The assignment expects this directory to be present before you start."
    )
    assert SAMPLE_DIR.is_dir(), (
        f"{SAMPLE_DIR} exists but is not a directory."
    )


def test_sample_file_exists_and_is_readable():
    """
    The file /home/user/sample_configs/sshd_config must exist, be a regular file,
    and be readable by the current user.
    """
    assert SAMPLE_FILE.exists(), (
        f"Required file {SAMPLE_FILE} is missing. "
        "Make sure the initial sample configuration file is in place."
    )
    assert SAMPLE_FILE.is_file(), (
        f"{SAMPLE_FILE} exists but is not a regular file."
    )

    # Check read permission for the current user
    st_mode = SAMPLE_FILE.stat().st_mode
    is_readable = bool(st_mode & (stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH))
    assert is_readable, (
        f"{SAMPLE_FILE} is not readable; please ensure it has read permissions."
    )


def test_sample_file_contains_expected_markers():
    """
    The sample sshd_config should still contain the default (insecure) settings
    that the student is tasked with hardening.

    Specifically, we expect:
      * An uncommented line 'PermitRootLogin yes'
      * An uncommented line 'PasswordAuthentication yes'
    And we do *not* expect their hardened counterparts to be present yet.
    """
    content = SAMPLE_FILE.read_text().splitlines()

    # Helper to locate uncommented config directives
    def has_uncommented_line(expected_line: str) -> bool:
        return any(
            line.strip() == expected_line
            for line in content
            if not line.lstrip().startswith("#")
        )

    assert has_uncommented_line("PermitRootLogin yes"), (
        f"{SAMPLE_FILE} should still contain an uncommented line 'PermitRootLogin yes' "
        "before hardening begins."
    )
    assert has_uncommented_line("PasswordAuthentication yes"), (
        f"{SAMPLE_FILE} should still contain an uncommented line 'PasswordAuthentication yes' "
        "before hardening begins."
    )

    # Ensure hardened counterparts are NOT present yet
    assert not has_uncommented_line("PermitRootLogin no"), (
        f"{SAMPLE_FILE} already contains 'PermitRootLogin no'. "
        "The hardening should occur only after the initial checks."
    )
    assert not has_uncommented_line("PasswordAuthentication no"), (
        f"{SAMPLE_FILE} already contains 'PasswordAuthentication no'. "
        "The hardening should occur only after the initial checks."
    )