# test_initial_state.py
#
# This test-suite verifies that the operating-system / file-system is in the
# expected *initial* state before the student starts working on ticket
# “INC10234”.
#
# What must be true BEFORE any action:
#
# 1. /home/user/it_support/firewall/allow_rules.list
#    – File exists.
#    – Contains exactly the three default firewall rules (and nothing else).
#      "# Firewall Allow Rules\n"
#      "ALLOW_TCP 22\n"
#      "ALLOW_TCP 443\n"
#    – Must *not* yet contain the “ALLOW_TCP 9000” rule.
#
# 2. /home/user/it_support/logs
#    – Directory exists and is writable by the current user.
#
# 3. /home/user/it_support/logs/INC10234_action.log
#    – File must NOT exist yet; it will be created by the student.
#
# If any of these conditions fail, the test output will clearly state what is
# wrong with the initial environment.

import os
import pytest


FIREWALL_RULES_PATH = "/home/user/it_support/firewall/allow_rules.list"
LOGS_DIR = "/home/user/it_support/logs"
TICKET_LOG_PATH = os.path.join(LOGS_DIR, "INC10234_action.log")


def test_firewall_rules_file_exists_and_has_expected_content():
    """
    The firewall rule list must exist and contain ONLY the default rules.
    """
    assert os.path.isfile(FIREWALL_RULES_PATH), (
        f"Missing firewall rule file: {FIREWALL_RULES_PATH}"
    )

    with open(FIREWALL_RULES_PATH, encoding="utf-8") as fp:
        content = fp.read()

    expected_content = (
        "# Firewall Allow Rules\n"
        "ALLOW_TCP 22\n"
        "ALLOW_TCP 443\n"
    )

    assert content == expected_content, (
        "The firewall rule file does not match the expected *initial* content.\n"
        "Expected exactly:\n"
        f"{expected_content!r}\n"
        "But found:\n"
        f"{content!r}"
    )

    assert "ALLOW_TCP 9000" not in content, (
        "Port 9000 is already present in the rule file, "
        "but it should only be added by the student."
    )


def test_logs_directory_exists_and_is_writable():
    """
    The logs directory must exist and be writable by the current user.
    """
    assert os.path.isdir(LOGS_DIR), f"Missing logs directory: {LOGS_DIR}"

    # Check write permission without creating files.
    assert os.access(LOGS_DIR, os.W_OK), (
        f"The logs directory '{LOGS_DIR}' is not writable."
    )


def test_ticket_log_file_is_absent():
    """
    The specific ticket log file should NOT exist yet.
    """
    assert not os.path.exists(TICKET_LOG_PATH), (
        f"The ticket log file '{TICKET_LOG_PATH}' already exists; "
        "it should be created by the student's solution."
    )