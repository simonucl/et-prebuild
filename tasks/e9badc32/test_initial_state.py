# test_initial_state.py
#
# This pytest suite verifies the **initial** state of the simulated
# environment *before* the student runs any command.
#
# 1.  /home/user/current_firewall.txt must exist and contain the exact
#     ip-tables rule-set specified in the task description.
# 2.  That file must include exactly three non-comment rules that both
#     contain the substring “ACCEPT” and “dport 443”.
# 3.  /home/user/port443_count.log must *not* exist yet – it will be
#     created by the student during the assignment.
#
# Only the Python standard library and pytest are used.

import os
from pathlib import Path

import pytest

# Absolute paths that are referenced in the assignment
FIREWALL_FILE = Path("/home/user/current_firewall.txt")
OUTPUT_LOG = Path("/home/user/port443_count.log")

# The canonical, ground-truth contents of /home/user/current_firewall.txt
EXPECTED_FIREWALL_LINES = [
    ":INPUT ACCEPT [0:0]",
    ":FORWARD ACCEPT [0:0]",
    ":OUTPUT ACCEPT [0:0]",
    "-A INPUT -p tcp -m tcp --dport 80  -j ACCEPT",
    "-A INPUT -p tcp -m tcp --dport 443 -j ACCEPT",
    "-A INPUT -p tcp -m tcp --dport 22  -j ACCEPT",
    "-A INPUT -p tcp -m tcp --dport 443 -j ACCEPT",
    "-A INPUT -p tcp -m tcp --dport 8080 -j DROP",
    "-A INPUT -p tcp -m tcp --dport 443 -j ACCEPT",
]


@pytest.fixture(scope="module")
def firewall_content():
    """
    Read and return the firewall file content as a list of lines without
    trailing newlines.  The fixture fails early with a clear message if
    the file is missing.
    """
    if not FIREWALL_FILE.exists():
        pytest.fail(
            f"Required file {FIREWALL_FILE} is missing. "
            "The initial environment must ship with the exported firewall rules."
        )

    if not FIREWALL_FILE.is_file():
        pytest.fail(f"{FIREWALL_FILE} exists but is not a regular file.")

    # Read file, strip the final newline of each line
    with FIREWALL_FILE.open("r", encoding="utf-8") as fh:
        lines = [ln.rstrip("\n") for ln in fh.readlines()]
    return lines


def test_firewall_file_has_expected_content(firewall_content):
    """
    Ensure /home/user/current_firewall.txt exactly matches the ground-truth
    provided in the task description.
    """
    assert (
        firewall_content == EXPECTED_FIREWALL_LINES
    ), (
        "The contents of /home/user/current_firewall.txt do not match the "
        "expected initial firewall rule-set."
    )


def test_exactly_three_accept_443_rules(firewall_content):
    """
    Confirm that the file contains exactly three non-comment rules that
    (1) contain 'ACCEPT' and (2) reference destination port 443.
    """
    count = 0
    for line in firewall_content:
        stripped = line.lstrip()
        if stripped.startswith("#"):
            # Ignore comment lines entirely
            continue
        if "ACCEPT" in stripped and "dport 443" in stripped:
            count += 1

    assert count == 3, (
        f"Expected exactly 3 ACCEPT rules targeting port 443, "
        f"but found {count}."
    )


def test_output_log_not_present_initially():
    """
    The result file should not exist before the student executes their
    one-liner command.
    """
    assert not OUTPUT_LOG.exists(), (
        f"{OUTPUT_LOG} should not exist yet. "
        "It must be created by the student's command."
    )