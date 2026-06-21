# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state before the
# learner performs any action.  It checks that the required directories
# and the baseline firewall rules file exist exactly as specified, and
# that the change-tracking log file is **absent**.
#
# If any test fails, the assertion message will explain precisely what
# is wrong so the learner can fix the starting environment.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
CONFIG_DIR = HOME / "config"
LOGS_DIR = HOME / "logs"
FIREWALL_RULES = CONFIG_DIR / "firewall.rules"
ACTIONS_LOG = LOGS_DIR / "firewall_actions.log"

EXPECTED_FIREWALL_CONTENT = (
    "-A INPUT -p tcp --dport 22 -j ACCEPT\n"
    "-A INPUT -j DROP\n"
)


@pytest.fixture(scope="module")
def firewall_rules_text():
    """Read the firewall.rules file once for all tests."""
    if not FIREWALL_RULES.exists():
        pytest.fail(f"Missing expected file: {FIREWALL_RULES}")
    try:
        return FIREWALL_RULES.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Could not read {FIREWALL_RULES}: {exc}")


def test_config_directory_exists():
    assert CONFIG_DIR.exists(), f"Expected directory does not exist: {CONFIG_DIR}"
    assert CONFIG_DIR.is_dir(), f"{CONFIG_DIR} exists but is not a directory"


def test_logs_directory_exists():
    assert LOGS_DIR.exists(), f"Expected directory does not exist: {LOGS_DIR}"
    assert LOGS_DIR.is_dir(), f"{LOGS_DIR} exists but is not a directory"


def test_firewall_rules_file_exists():
    assert FIREWALL_RULES.exists(), f"Expected file does not exist: {FIREWALL_RULES}"
    assert FIREWALL_RULES.is_file(), f"{FIREWALL_RULES} exists but is not a regular file"


def test_firewall_rules_content_exact(firewall_rules_text):
    actual = firewall_rules_text
    assert actual == EXPECTED_FIREWALL_CONTENT, (
        "The initial firewall.rules file must contain exactly two lines "
        "followed by a terminating newline:\n"
        "1) -A INPUT -p tcp --dport 22 -j ACCEPT\n"
        "2) -A INPUT -j DROP\n"
        "Any deviation (extra lines, missing newline, leading/trailing "
        "whitespace) will fail this test."
    )


def test_firewall_actions_log_absent():
    assert not ACTIONS_LOG.exists(), (
        f"The change-tracking log {ACTIONS_LOG} should NOT exist in the "
        "initial state."
    )