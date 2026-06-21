# test_initial_state.py
#
# Pytest suite that validates the *initial* filesystem / OS state
# for the “mini-firewall” exercise **before** the student performs
# any actions.  The tests assert that:
#
# 1. The working directory /home/user/firewall_task exists.
# 2. Exactly two items are present in that directory:
#       • firewall.rules
#       • README.txt
#    (No firewall_debug.log should exist yet.)
# 3. /home/user/firewall_task/firewall.rules contains the *original*
#    rule set – i.e. it allows only port 80 (no port 8080 rule) and
#    the COMMIT line terminates the file.
# 4. There is no lingering port-8080 ACCEPT rule in the rules file.
#
# The tests rely solely on the Python stdlib + pytest.
#
# To run:
#     pytest -q
#
# Any failure message is crafted to tell the learner exactly what
# prerequisite is missing or wrong before they start the task.


import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
TASK_DIR = HOME / "firewall_task"
RULES_FILE = TASK_DIR / "firewall.rules"
README_FILE = TASK_DIR / "README.txt"
DEBUG_FILE = TASK_DIR / "firewall_debug.log"

ORIGINAL_RULES_CONTENT = (
    "*filter\n"
    ":INPUT DROP [0:0]\n"
    ":FORWARD DROP [0:0]\n"
    ":OUTPUT ACCEPT [0:0]\n"
    "-A INPUT -p tcp --dport 80 -j ACCEPT\n"
    "COMMIT\n"
)


def test_task_directory_exists():
    """firewall_task directory must exist and be a directory."""
    assert TASK_DIR.exists(), f"Expected directory {TASK_DIR} is missing."
    assert TASK_DIR.is_dir(), f"{TASK_DIR} exists but is not a directory."


def test_expected_files_present_and_only_them():
    """Exactly firewall.rules and README.txt should be present initially."""
    assert RULES_FILE.exists(), f"Expected rules file {RULES_FILE} is missing."
    assert README_FILE.exists(), f"Expected README file {README_FILE} is missing."
    # Collect item names in directory
    present_items = sorted(p.name for p in TASK_DIR.iterdir())
    expected_items = sorted([RULES_FILE.name, README_FILE.name])
    # DEBUG_FILE must not exist yet
    assert DEBUG_FILE.name not in present_items, (
        f"{DEBUG_FILE} should not exist before the task is done."
    )
    # Verify no other unexpected files/dirs
    unexpected = set(present_items) - set(expected_items)
    assert (
        not unexpected
    ), f"Unexpected items present in {TASK_DIR}: {', '.join(unexpected)}"


def test_firewall_rules_original_content():
    """firewall.rules should match the exact original content."""
    with RULES_FILE.open("r", encoding="utf-8") as fh:
        content = fh.read()

    # Strip nothing; we want exact match including trailing newline.
    assert (
        content == ORIGINAL_RULES_CONTENT
    ), (
        "The current content of firewall.rules does not match the expected "
        "original starting state.\n\n"
        "Expected:\n"
        f"{ORIGINAL_RULES_CONTENT!r}\n\n"
        "Found:\n"
        f"{content!r}"
    )


def test_no_8080_rule_yet():
    """There must be no ACCEPT rule for port 8080 before the student acts."""
    rules_text = RULES_FILE.read_text(encoding="utf-8")
    illegal_line = "-A INPUT -p tcp --dport 8080 -j ACCEPT"
    assert (
        illegal_line not in rules_text
    ), f"Unexpected port-8080 rule already present in {RULES_FILE}."


def test_debug_log_not_present():
    """firewall_debug.log must not exist yet."""
    assert (
        not DEBUG_FILE.exists()
    ), f"{DEBUG_FILE} should not be present before the task is started."