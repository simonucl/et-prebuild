# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem
# state before the student performs any action for the “iptables 8088 rule”
# exercise.  All tests must pass **before** the learner starts working.

import os
import pytest
import textwrap

IPTABLES_PATH = "/home/user/deployment/firewall/iptables.rules"
LOGS_DIR      = "/home/user/deployment/logs"
UPDATE_LOG    = os.path.join(LOGS_DIR, "firewall_update.log")


@pytest.fixture(scope="module")
def iptables_contents():
    """
    Read the iptables file once per module and return its content as a list
    of stripped lines (no trailing newlines).
    """
    if not os.path.exists(IPTABLES_PATH):
        pytest.fail(
            f"Required iptables rule file not found at {IPTABLES_PATH!r}. "
            "The file must exist before the exercise begins."
        )
    if not os.path.isfile(IPTABLES_PATH):
        pytest.fail(
            f"{IPTABLES_PATH!r} exists but is not a regular file. "
            "It must be a writable plain-text file."
        )
    with open(IPTABLES_PATH, encoding="utf-8") as fh:
        return [line.rstrip("\n") for line in fh.readlines()]


def test_expected_default_iptables_content(iptables_contents):
    """
    Validate that the iptables rule file matches the *initial* specification
    (i.e. contains only the default SSH rule and *no* 8088 rule yet).
    """
    expected = textwrap.dedent(
        """\
        *filter
        :INPUT DROP [0:0]
        :FORWARD DROP [0:0]
        :OUTPUT ACCEPT [0:0]
        -A INPUT -p tcp --dport 22 -j ACCEPT
        COMMIT"""
    ).splitlines()

    assert iptables_contents == expected, (
        "The current contents of "
        f"{IPTABLES_PATH!r} do not match the expected initial state.\n\n"
        "Expected:\n"
        + "\n".join(expected)
        + "\n\nActual:\n"
        + "\n".join(iptables_contents)
    )


def test_no_8088_rule_yet(iptables_contents):
    """
    Ensure the new 8088 ACCEPT rule has *not* been added yet.
    """
    forbidden_rule = "-A INPUT -p tcp --dport 8088 -j ACCEPT"
    assert forbidden_rule not in iptables_contents, (
        f"Found unexpected rule {forbidden_rule!r} in {IPTABLES_PATH!r}. "
        "The file should be unmodified before the student starts."
    )


def test_logs_directory_exists():
    """
    The change-tracking directory must already exist.
    """
    assert os.path.isdir(LOGS_DIR), (
        f"Expected directory {LOGS_DIR!r} is missing. "
        "Create this directory as part of the initial project scaffold."
    )


def test_update_log_not_present_yet():
    """
    The firewall_update.log file must **not** exist before any work is done.
    """
    assert not os.path.exists(UPDATE_LOG), (
        f"Found unexpected file {UPDATE_LOG!r}. "
        "The update log should be created only after the new rule is added."
    )