# test_initial_state.py
#
# Pytest suite that verifies the machine’s initial state **before**
# the student executes any hardening commands.
#
# What we validate:
# 1. /home/user/insecure_config/ exists and is a directory.
# 2. /home/user/insecure_config/sshd_config exists and is a regular file.
# 3. The file contains exactly two (and only two) lines, in this
#    precise order:
#       PermitRootLogin yes
#       PasswordAuthentication yes
#
# We deliberately do *not* test for the presence or absence of any
# output artifacts (e.g., /home/user/secure_config/, sshd_config_hardened,
# or hardening.log), in accordance with the grading policy.

from pathlib import Path
import pytest

INSECURE_DIR = Path("/home/user/insecure_config")
SSHD_CONFIG = INSECURE_DIR / "sshd_config"


def test_insecure_config_directory_exists():
    """The insecure configuration directory must already exist."""
    assert INSECURE_DIR.exists(), (
        f"Required directory {INSECURE_DIR} is missing."
    )
    assert INSECURE_DIR.is_dir(), (
        f"{INSECURE_DIR} exists but is not a directory."
    )


def test_sshd_config_file_exists():
    """The insecure sshd_config file must already be present."""
    assert SSHD_CONFIG.exists(), (
        f"Required file {SSHD_CONFIG} is missing."
    )
    assert SSHD_CONFIG.is_file(), (
        f"{SSHD_CONFIG} exists but is not a regular file."
    )


def test_sshd_config_contents():
    """
    The sshd_config file must contain exactly the two expected
    insecure lines and nothing else (aside from an optional
    trailing newline).
    """
    contents = SSHD_CONFIG.read_text().splitlines()

    expected_lines = [
        "PermitRootLogin yes",
        "PasswordAuthentication yes",
    ]

    assert contents == expected_lines, (
        f"Unexpected contents in {SSHD_CONFIG}.\n"
        f"Expected exactly:\n"
        f"    {expected_lines[0]}\n"
        f"    {expected_lines[1]}\n"
        f"Got:\n"
        + "\n".join(f"    {line}" for line in contents)
    )