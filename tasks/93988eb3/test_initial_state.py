# test_initial_state.py
#
# Pytest suite that validates the operating-system / filesystem _before_
# the student runs their solution.  It confirms the presence of the
# firewall rule-set and the absence of the audit artefacts.
#
# Requirements verified:
#   1. /home/user/firewall  directory exists            (pre-provided)
#   2. /home/user/firewall/iptables.rules file exists   (pre-provided)
#   3. iptables.rules contains at least one INPUT-chain rule that
#      allows TCP traffic on destination port 22 (dport 22) and ACCEPTs it
#   4. /home/user/audit directory does NOT yet exist
#   5. /home/user/audit/ssh_port_status.log does NOT yet exist
#
# Only stdlib + pytest are used.

import os
import re
import pathlib
import pytest

FIREWALL_DIR = '/home/user/firewall'
RULES_FILE = os.path.join(FIREWALL_DIR, 'iptables.rules')
AUDIT_DIR = '/home/user/audit'
LOG_FILE = os.path.join(AUDIT_DIR, 'ssh_port_status.log')


def test_firewall_directory_exists():
    assert os.path.isdir(FIREWALL_DIR), (
        f"Expected firewall directory '{FIREWALL_DIR}' to exist, "
        "but it is missing."
    )


def test_rules_file_exists():
    assert os.path.isfile(RULES_FILE), (
        f"Expected rules file '{RULES_FILE}' to exist, but it is missing."
    )


def test_rules_file_allows_ssh_port_22():
    """
    Confirm that at least one INPUT-chain rule explicitly allows
    TCP traffic to destination port 22 (SSH) and jumps to ACCEPT.
    """
    with open(RULES_FILE, 'r', encoding='utf-8', errors='ignore') as fh:
        lines = fh.readlines()

    # Regex explanation:
    #   ^-A INPUT         -> rule in the INPUT chain
    #   .*?               -> anything (non-greedy)
    #   -p\s+tcp          -> protocol TCP
    #   .*?               -> anything
    #   --dport\s+22      -> destination port 22
    #   .*?               -> anything
    #   -j\s+ACCEPT       -> target ACCEPT
    rule_re = re.compile(
        r'^-A\s+INPUT\b.*?-p\s+tcp\b.*?--dport\s+22\b.*?-j\s+ACCEPT\b',
        flags=re.IGNORECASE
    )

    matching_rules = [ln.strip() for ln in lines if rule_re.search(ln)]
    assert matching_rules, (
        "No INPUT-chain rule found in iptables.rules that explicitly allows "
        "TCP traffic on port 22 (SSH). Expected at least one rule such as "
        "'-A INPUT -p tcp --dport 22 -j ACCEPT'."
    )


def test_audit_directory_absent():
    assert not os.path.exists(AUDIT_DIR), (
        f"Audit directory '{AUDIT_DIR}' should NOT exist before the student "
        "runs their command, but it was found."
    )


def test_log_file_absent():
    assert not os.path.exists(LOG_FILE), (
        f"Log file '{LOG_FILE}' should NOT exist before the student "
        "runs their command, but it was found."
    )