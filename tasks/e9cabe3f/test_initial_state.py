# test_initial_state.py
#
# This pytest suite validates the **initial** state of the filesystem
# before the student performs any actions.  It checks that the expected
# directory and the exported base_rules.v4 file exist and that
# base_rules.v4 has the exact, unmodified iptables-save contents that
# were provided in the task description.
#
# NOTE:  Per the instructions, this suite intentionally does **not**
#        make any assertions about the *output* artefacts
#        (optimized_rules.v4, change_log.csv); it only inspects the
#        starting conditions.

import os
from pathlib import Path

import pytest


FIREWALL_DIR = Path("/home/user/firewall")
BASE_RULES = FIREWALL_DIR / "base_rules.v4"

# Expected content of base_rules.v4 *including* the terminating newline
EXPECTED_BASE_RULES_LINES = [
    "*filter\n",
    ":INPUT ACCEPT [0:0]\n",
    ":FORWARD ACCEPT [0:0]\n",
    ":OUTPUT ACCEPT [0:0]\n",
    "-A INPUT -p tcp --dport 22 -j ACCEPT\n",
    "-A INPUT -p tcp --dport 80 -j ACCEPT\n",
    "-A INPUT -p tcp --dport 443 -j ACCEPT\n",
    "-A INPUT -p tcp --dport 8080 -j ACCEPT\n",
    "-A INPUT -p tcp --dport 3306 -j ACCEPT\n",
    "COMMIT\n",
]


def test_firewall_directory_exists():
    assert FIREWALL_DIR.exists(), (
        f"Required directory {FIREWALL_DIR} is missing. "
        "The task assumes this directory already exists."
    )
    assert FIREWALL_DIR.is_dir(), f"{FIREWALL_DIR} exists but is not a directory."


def test_base_rules_file_exists():
    assert BASE_RULES.exists(), (
        f"Required file {BASE_RULES} is missing. "
        "The base firewall rules must be present before any modifications."
    )
    assert BASE_RULES.is_file(), f"{BASE_RULES} exists but is not a regular file."


def test_base_rules_contents_are_exact():
    with BASE_RULES.open("r", encoding="utf-8") as fh:
        lines = fh.readlines()

    # Helpful diff in assertion if mismatch occurs
    assert lines == EXPECTED_BASE_RULES_LINES, (
        f"{BASE_RULES} does not match the expected initial content.\n"
        f"Expected ({len(EXPECTED_BASE_RULES_LINES)} lines):\n"
        + "".join(EXPECTED_BASE_RULES_LINES)
        + "\nActual ({len(lines)} lines):\n"
        + "".join(lines)
    )


@pytest.mark.parametrize(
    "expected_line",
    [
        ":INPUT ACCEPT [0:0]\n",
        ":FORWARD ACCEPT [0:0]\n",
        ":OUTPUT ACCEPT [0:0]\n",
    ],
)
def test_default_policies_are_accept(expected_line):
    """
    Ensure that the default policies in the *initial* rules are all ACCEPT.
    """
    with BASE_RULES.open("r", encoding="utf-8") as fh:
        contents = fh.read()
    assert (
        expected_line in contents
    ), f"Expected default policy line '{expected_line.rstrip()}' not found in {BASE_RULES}"


@pytest.mark.parametrize(
    "port_line",
    [
        "-A INPUT -p tcp --dport 22 -j ACCEPT\n",
        "-A INPUT -p tcp --dport 80 -j ACCEPT\n",
        "-A INPUT -p tcp --dport 443 -j ACCEPT\n",
        "-A INPUT -p tcp --dport 8080 -j ACCEPT\n",
        "-A INPUT -p tcp --dport 3306 -j ACCEPT\n",
    ],
)
def test_all_expected_accept_rules_present(port_line):
    """
    Verify the presence of every ACCEPT rule that should be in the initial export.
    """
    with BASE_RULES.open("r", encoding="utf-8") as fh:
        contents = fh.read()
    assert (
        port_line in contents
    ), f"Expected rule line '{port_line.rstrip()}' missing from {BASE_RULES}"


def test_file_ends_with_commit_newline():
    with BASE_RULES.open("rb") as fh:
        fh.seek(0, os.SEEK_END)
        if fh.tell() == 0:
            pytest.fail(f"{BASE_RULES} is empty")
        # Read the last len('COMMIT\n') bytes
        fh.seek(-7, os.SEEK_END)
        tail = fh.read().decode("utf-8", errors="replace")
    assert (
        tail == "COMMIT\n"
    ), f"{BASE_RULES} must end with 'COMMIT' followed by a newline. Found tail: {tail!r}"