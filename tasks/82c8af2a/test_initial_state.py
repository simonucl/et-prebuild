# test_initial_state.py
#
# This pytest suite validates the **initial** filesystem/OS state *before*
# the learner performs any actions.  It checks only the pre-existing,
# “given” resources and intentionally ignores (does not look for)
# any output artefacts that the learner is expected to create later
# (patch files, logs, etc.).
#
# Only the Python standard library and pytest are used.

import os
import pytest

BASE_DIR = "/home/user/network_configs"
BASELINE_CFG = os.path.join(BASE_DIR, "baseline", "router.conf")
CURRENT_CFG = os.path.join(BASE_DIR, "current", "router.conf")


@pytest.fixture(scope="session")
def baseline_text():
    """Return the full text of the baseline/router.conf file."""
    if not os.path.isfile(BASELINE_CFG):
        pytest.fail(f"Missing baseline configuration file at {BASELINE_CFG}")
    with open(BASELINE_CFG, "r", encoding="utf-8") as fh:
        return fh.read()


@pytest.fixture(scope="session")
def current_text():
    """Return the full text of the current/router.conf file."""
    if not os.path.isfile(CURRENT_CFG):
        pytest.fail(f"Missing current configuration file at {CURRENT_CFG}")
    with open(CURRENT_CFG, "r", encoding="utf-8") as fh:
        return fh.read()


def test_baseline_has_expected_good_lines(baseline_text):
    """
    The baseline configuration must contain the authoritative,
    ‘known-good’ statements.
    """
    required_lines = [
        " ip address 10.0.0.1/24",
        " no shutdown",
        " network 10.0.0.0 0.0.0.255 area 0",
        " network 192.168.1.0 0.0.0.255 area 0",
    ]
    for line in required_lines:
        assert (
            line in baseline_text.splitlines()
        ), f"Baseline config is missing expected line: {line!r}"


def test_current_has_expected_bad_lines(current_text):
    """
    The current (broken) configuration must exhibit the incorrect
    statements that the learner is asked to fix.
    """
    expected_present = [
        " ip address 10.0.0.2/24",
        " shutdown",
        " network 10.0.0.0 0.0.0.255 area 0",
    ]
    expected_absent = [
        " ip address 10.0.0.1/24",
        " no shutdown",
        " network 192.168.1.0 0.0.0.255 area 0",
    ]

    cur_lines = current_text.splitlines()

    for line in expected_present:
        assert (
            line in cur_lines
        ), f"Current config should contain {line!r} but does not."

    for line in expected_absent:
        assert (
            line not in cur_lines
        ), f"Current config unexpectedly contains {line!r}; it should not be there yet."


def test_baseline_and_current_differ(baseline_text, current_text):
    """
    Sanity-check that the baseline and current files are *not* already identical;
    otherwise there would be nothing to fix.
    """
    assert (
        baseline_text != current_text
    ), "Baseline and current configuration files are already identical; nothing to patch."