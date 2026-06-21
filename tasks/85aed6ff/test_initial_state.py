# test_initial_state.py
#
# This pytest suite validates the filesystem BEFORE the student
# performs any action on the task.  It ensures that the expected
# directory structure, files, permissions and initial contents are
# present exactly as specified.

import os
import stat
import pytest

HOME_DIR = "/home/user"
FIREWALL_DIR = os.path.join(HOME_DIR, "firewall")
ACTIVE_RULES = os.path.join(FIREWALL_DIR, "active_rules.sh")
CHANGE_LOG = os.path.join(FIREWALL_DIR, "change_log.txt")


def _mode(path):
    "Return the octal permission bits (e.g. 0o644) for a given path."
    return stat.S_IMODE(os.stat(path).st_mode)


def test_firewall_directory_exists():
    assert os.path.isdir(FIREWALL_DIR), (
        f"Expected directory {FIREWALL_DIR} to exist "
        "before any changes are made."
    )


def test_active_rules_file_exists_with_correct_permissions():
    assert os.path.isfile(ACTIVE_RULES), (
        f"Expected file {ACTIVE_RULES} to exist before task execution."
    )
    expected_mode = 0o644
    actual_mode = _mode(ACTIVE_RULES)
    assert actual_mode == expected_mode, (
        f"{ACTIVE_RULES} permissions are {oct(actual_mode)}, "
        f"expected {oct(expected_mode)}."
    )


def test_active_rules_file_initial_contents():
    expected_content = (
        "#!/bin/bash\n"
        "# ACTIVE FIREWALL RULESET\n"
        "# Managed by config-team\n"
    )
    with open(ACTIVE_RULES, "r", encoding="utf-8") as fh:
        actual_content = fh.read()
    assert actual_content == expected_content, (
        f"{ACTIVE_RULES} does not contain the expected initial "
        "three-line header exactly as specified (including the final newline)."
    )


def test_change_log_exists_with_correct_permissions_and_empty():
    assert os.path.isfile(CHANGE_LOG), (
        f"Expected file {CHANGE_LOG} to exist before task execution."
    )
    expected_mode = 0o644
    actual_mode = _mode(CHANGE_LOG)
    assert actual_mode == expected_mode, (
        f"{CHANGE_LOG} permissions are {oct(actual_mode)}, "
        f"expected {oct(expected_mode)}."
    )

    with open(CHANGE_LOG, "rb") as fh:
        content = fh.read()
    assert content == b"", (
        f"{CHANGE_LOG} is expected to be an empty file (0 bytes) "
        "before any changes are made."
    )