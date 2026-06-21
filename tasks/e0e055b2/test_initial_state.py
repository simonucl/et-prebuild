# test_initial_state.py
#
# Pytest suite that validates the **initial** operating-system / filesystem
# state for the “iptables rule insertion” exercise.
#
# What we check (and nothing more):
#   1. Directory /home/user/firewall exists, is a directory, and has 0755 perms.
#   2. File /home/user/firewall/iptables_rules.v4 exists, has 0644 perms,
#      and its *exact* contents match the expected starting template.
#
# We intentionally do *not* look for /home/user/firewall/configuration.log
# because that file is an output of the student’s task, and the spec forbids
# asserting on output artefacts in the initial-state test.

import os
import stat
import textwrap
import pytest
from pathlib import Path

HOME = Path("/home/user")
FIREWALL_DIR = HOME / "firewall"
RULES_FILE = FIREWALL_DIR / "iptables_rules.v4"


def test_firewall_directory_exists_with_correct_permissions():
    """
    The directory /home/user/firewall must exist, be a directory,
    and have permission bits 0755.
    """
    assert FIREWALL_DIR.exists(), (
        f"Expected directory {FIREWALL_DIR} to exist, but it is missing."
    )
    assert FIREWALL_DIR.is_dir(), (
        f"Expected {FIREWALL_DIR} to be a directory, but it is not."
    )

    mode = FIREWALL_DIR.stat().st_mode & 0o777
    expected_mode = 0o755
    assert mode == expected_mode, (
        f"Directory {FIREWALL_DIR} has permissions {oct(mode)}, "
        f"expected {oct(expected_mode)}."
    )


def test_rules_file_exists_with_correct_permissions_and_content():
    """
    The iptables rules file must exist, be a file, have 0644 perms,
    and contain the exact, unmodified starter rules.
    """
    assert RULES_FILE.exists(), (
        f"Expected file {RULES_FILE} to exist, but it is missing."
    )
    assert RULES_FILE.is_file(), (
        f"Expected {RULES_FILE} to be a regular file, but it is not."
    )

    mode = RULES_FILE.stat().st_mode & 0o777
    expected_mode = 0o644
    assert mode == expected_mode, (
        f"File {RULES_FILE} has permissions {oct(mode)}, "
        f"expected {oct(expected_mode)}."
    )

    expected_content = textwrap.dedent(
        """\
        *filter
        :INPUT DROP [0:0]
        :FORWARD DROP [0:0]
        :OUTPUT ACCEPT [0:0]
        -A INPUT -p tcp --dport 22 -j ACCEPT
        COMMIT
        """
    )
    # Ensure the expected content ends with a newline character,
    # as typical tools write the last \n.
    if not expected_content.endswith("\n"):
        expected_content += "\n"

    with RULES_FILE.open("r", encoding="utf-8") as fh:
        actual_content = fh.read()

    assert actual_content == expected_content, (
        f"The content of {RULES_FILE} does not match the expected "
        f"initial template.\n\n--- Expected ---\n{expected_content}"
        f"--- Actual ---\n{actual_content}"
    )