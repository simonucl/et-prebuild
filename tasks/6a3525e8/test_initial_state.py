# test_initial_state.py
"""
Pytest suite that verifies the initial state of the workspace *before* the
student attempts the exercise.

It checks that:
1. The security directory exists.
2. `firewall_rules.conf` exists and contains exactly the two expected lines
   (with a single trailing newline).
3. `firewall_update.log` is **not** present yet.
4. The permissions of `firewall_rules.conf` are in the user-writable range
   (0600–0666) so that the student can modify it.

If any assertion fails, the error message explains precisely what is wrong.
"""

import os
from pathlib import Path
import stat
import pytest

SECURITY_DIR = Path("/home/user/project/security")
RULES_FILE = SECURITY_DIR / "firewall_rules.conf"
LOG_FILE = SECURITY_DIR / "firewall_update.log"

EXPECTED_RULES_CONTENT = "22/tcp ALLOW\n80/tcp ALLOW\n"


def test_security_directory_exists():
    assert SECURITY_DIR.is_dir(), (
        f"Expected directory '{SECURITY_DIR}' to exist but it was missing."
    )


def test_firewall_rules_file_exists():
    assert RULES_FILE.is_file(), (
        f"Expected file '{RULES_FILE}' to exist inside the security directory."
    )


def test_firewall_rules_file_content():
    """
    The file must contain exactly two lines:
        22/tcp ALLOW
        80/tcp ALLOW
    Each line ends with a single Unix newline and there are no extra lines.
    """
    content = RULES_FILE.read_text(encoding="utf-8")
    assert content == EXPECTED_RULES_CONTENT, (
        f"'{RULES_FILE}' content mismatch.\n"
        "Expected exactly:\n"
        f"{EXPECTED_RULES_CONTENT!r}\n"
        "But found:\n"
        f"{content!r}"
    )


def test_firewall_rules_file_permissions():
    """
    The file must be user-writable so that the student can edit it.
    We allow any permission in the inclusive range 0o600–0o666.
    """
    mode = RULES_FILE.stat().st_mode & 0o777
    assert 0o600 <= mode <= 0o666, (
        f"'{RULES_FILE}' permissions are {oct(mode)}, "
        "but they must be in the range 0o600–0o666 so the user can write to it."
    )


def test_update_log_not_present_yet():
    assert not LOG_FILE.exists(), (
        f"'{LOG_FILE}' should not exist before the student runs their command."
    )