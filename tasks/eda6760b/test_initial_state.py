# test_initial_state.py
#
# This test-suite validates the *initial* state of the filesystem
# before the student runs their single compound shell command.
#
# It confirms that:
#   1. /home/user/iptables.rules exists and is a regular file.
#   2. The file contains exactly one “COMMIT” line, which is the
#      final non-empty line of the file.
#   3. The new rule for port 8080 is **not** present yet.
#   4. The pre-existing rules for ports 22 and 80 are present.
#
# NOTE:  We deliberately do **not** test for /home/user/firewall_update.log
#        (or any other output artefacts) because those must not exist in
#        the initial state.

import os
from pathlib import Path
import pytest

IPTABLES_PATH = Path("/home/user/iptables.rules")
NEW_RULE = "-A INPUT -p tcp --dport 8080 -j ACCEPT"


def test_iptables_rules_file_exists():
    """The iptables.rules file must exist and be a regular file."""
    assert IPTABLES_PATH.exists(), f"Expected {IPTABLES_PATH} to exist, but it does not."
    assert IPTABLES_PATH.is_file(), f"Expected {IPTABLES_PATH} to be a regular file."


def test_initial_iptables_content():
    """Validate the initial contents of iptables.rules."""
    content = IPTABLES_PATH.read_text(encoding="utf-8").splitlines()

    # File must not be empty
    assert content, f"{IPTABLES_PATH} should not be empty."

    # Ensure exactly one 'COMMIT' line and it is last non-empty line
    commit_indices = [idx for idx, line in enumerate(content) if line == "COMMIT"]
    assert commit_indices, f"{IPTABLES_PATH} should contain a line 'COMMIT'."
    assert len(commit_indices) == 1, (
        f"{IPTABLES_PATH} should contain exactly one 'COMMIT' line, "
        f"found {len(commit_indices)}."
    )

    last_non_empty_idx = max(idx for idx, line in enumerate(content) if line.strip())
    assert (
        content[last_non_empty_idx] == "COMMIT"
    ), "'COMMIT' must be the final non-empty line in iptables.rules."

    # The new rule must **not** be present yet
    assert (
        NEW_RULE not in content
    ), f"{IPTABLES_PATH} should not yet contain the rule '{NEW_RULE}'."

    # Pre-existing rules for ports 22 and 80 must be present
    for port in (22, 80):
        rule = f"-A INPUT -p tcp --dport {port} -j ACCEPT"
        assert (
            rule in content
        ), f"Expected to find existing rule '{rule}' in {IPTABLES_PATH}, but it is missing."