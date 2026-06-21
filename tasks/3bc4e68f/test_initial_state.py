# test_initial_state.py
#
# Pytest suite that validates the **initial** state of the training
# environment for the “Prometheus / Grafana / node-exporter firewall”
# exercise.  The tests make sure that the required directory and the two
# specification files already exist *before* any further user action.
#
# Only the Python standard library and pytest are used.

import os
from pathlib import Path

# --------------------------------------------------------------------------------------
# CONSTANTS ― update these only if the exercise specification changes
# --------------------------------------------------------------------------------------

HOME = Path("/home/user")
FIREWALL_DIR = HOME / "firewall_configs"
RULES_FILE = FIREWALL_DIR / "iptables_prometheus.rules"
REPORT_FILE = HOME / "report_firewall.log"

EXPECTED_RULES = (
    "*filter\n"
    ":INPUT DROP [0:0]\n"
    ":FORWARD DROP [0:0]\n"
    ":OUTPUT ACCEPT [0:0]\n"
    "-A INPUT -p tcp --dport 22   -j ACCEPT\n"
    "-A INPUT -p tcp --dport 9090 -j ACCEPT\n"
    "-A INPUT -p tcp --dport 3000 -j ACCEPT\n"
    "-A INPUT -p tcp --dport 9100 -j ACCEPT\n"
    "COMMIT\n"
)

EXPECTED_REPORT = (
    "22,ALLOWED\n"
    "9090,ALLOWED\n"
    "3000,ALLOWED\n"
    "9100,ALLOWED\n"
    "3306,DENIED\n"
)

# --------------------------------------------------------------------------------------
# TESTS
# --------------------------------------------------------------------------------------


def test_firewall_directory_exists():
    """
    Validate that /home/user/firewall_configs exists and is a directory.
    """
    assert FIREWALL_DIR.exists(), (
        f"Required directory {FIREWALL_DIR} is missing. "
        "Create it with the exact name and path."
    )
    assert FIREWALL_DIR.is_dir(), (
        f"{FIREWALL_DIR} exists but is not a directory."
    )


def test_rules_file_exact_content():
    """
    Validate that iptables_prometheus.rules exists *and* matches the
    specification byte-for-byte (including the trailing newline).
    """
    assert RULES_FILE.exists(), (
        f"Rules file {RULES_FILE} is missing."
    )
    assert RULES_FILE.is_file(), (
        f"{RULES_FILE} exists but is not a regular file."
    )

    actual = RULES_FILE.read_bytes()
    expected = EXPECTED_RULES.encode("utf-8")

    assert actual == expected, (
        f"Content of {RULES_FILE} does not match the required iptables rules.\n"
        "Use the exact lines, order, spacing, and be sure to include the final newline."
    )


def test_report_file_exact_content():
    """
    Validate that report_firewall.log exists and contains the five
    required CSV lines in the specified order.
    """
    assert REPORT_FILE.exists(), f"Report file {REPORT_FILE} is missing."
    assert REPORT_FILE.is_file(), (
        f"{REPORT_FILE} exists but is not a regular file."
    )

    actual = REPORT_FILE.read_text(encoding="utf-8")
    assert actual == EXPECTED_REPORT, (
        f"Content of {REPORT_FILE} is incorrect.\n"
        "It must contain exactly the following five lines (including newlines):\n"
        f"{EXPECTED_REPORT}"
    )