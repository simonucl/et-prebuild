# test_initial_state.py
#
# This pytest suite validates the **initial** state of the VM _before_
# the student executes any shell command for the task “open TCP port 5432”.
#
# The tests assert that:
#   1. /home/user/firewall.conf exists and contains the exact baseline rules.
#   2. The new rule for port 5432 is NOT present yet.
#   3. /home/user/firewall_update.log does **not** exist (or is empty).
#
# Any failure will provide a clear explanation of what is missing or incorrect.
#
# NOTE: Do **not** modify these tests; they describe the required starting state
#       and will be used by the automated checker to ensure a clean slate.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
FW_CONF = HOME / "firewall.conf"
FW_LOG = HOME / "firewall_update.log"

# The expected pristine contents of /home/user/firewall.conf
EXPECTED_FW_CONF_LINES = [
    "*filter",
    ":INPUT DROP [0:0]",
    ":FORWARD DROP [0:0]",
    ":OUTPUT ACCEPT [0:0]",
    "",
    "# Allow SSH",
    "-A INPUT -p tcp --dport 22 -j ACCEPT",
    "",
    "# DB RULES",
    "",
    "COMMIT",
]


def read_conf_lines(path: Path):
    """
    Read the firewall config and return the lines without trailing newlines.
    An empty line becomes an empty string '' in the resulting list.
    """
    with path.open("r", encoding="utf-8") as fh:
        # `splitlines()` drops the newline characters and keeps
        # blank lines as '', which is exactly what we want.
        return fh.read().splitlines()


def test_firewall_conf_exists():
    """The firewall configuration file must exist."""
    assert FW_CONF.exists(), f"Expected {FW_CONF} to exist, but it is missing."


def test_firewall_conf_pristine_contents():
    """
    The firewall configuration file must match the expected initial contents
    exactly.  This guards against pre-existing modifications.
    """
    lines = read_conf_lines(FW_CONF)
    assert (
        lines == EXPECTED_FW_CONF_LINES
    ), (
        f"{FW_CONF} does not match the required initial contents.\n"
        "Differences:\n"
        f"Expected:\n{EXPECTED_FW_CONF_LINES}\n\nActual:\n{lines}"
    )


def test_no_5432_rule_yet():
    """Ensure the rule for port 5432 is NOT present before the task begins."""
    lines = read_conf_lines(FW_CONF)
    rule_line = "-A INPUT -p tcp --dport 5432 -j ACCEPT"
    assert (
        rule_line not in lines
    ), f"Found unexpected rule for port 5432 in {FW_CONF} before the task started."


def test_log_file_absent_or_empty():
    """
    The log file should not exist (or should be completely empty)
    before the student runs the required single command.
    """
    if not FW_LOG.exists():
        # Perfect: the file isn't there yet.
        return

    # If it does exist, it must be empty.
    size = FW_LOG.stat().st_size
    assert (
        size == 0
    ), f"{FW_LOG} already exists with {size} bytes; it should not exist or must be empty before the task starts."