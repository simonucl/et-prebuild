# test_initial_state.py
#
# This pytest suite validates that the *initial* filesystem state is
# exactly as expected *before* the student begins any work.  It checks
# only the pre-existing resources and deliberately avoids asserting
# anything about the output artefacts that the student will later
# create (inventory.json, open_ports.log).

import os
import stat
import re
from pathlib import Path

import pytest

# Canonical absolute paths used throughout the tests
POLICY_DIR = Path("/home/user/devsecops/policy")
INVENTORY_TXT = POLICY_DIR / "inventory.txt"

# Expected baseline contents of inventory.txt
EXPECTED_LINES = [
    "22:ssh/tcp",
    "53:dns/udp",
    "80:http/tcp",
    "443:https/tcp",
    "8080:http-alt/tcp",
]

LINE_REGEX = re.compile(r"^\d+:[A-Za-z0-9-]+/[A-Za-z0-9]+$")


def test_policy_directory_exists_and_permissions():
    """
    The policy directory must exist, be a directory, and have mode 0755.
    """
    assert POLICY_DIR.exists(), f"Required directory not found: {POLICY_DIR!s}"
    assert POLICY_DIR.is_dir(), f"Expected a directory at {POLICY_DIR!s}, but found something else."

    # Check permissions (only the lower 3 octets matter; mask off file-type bits)
    mode = POLICY_DIR.stat().st_mode & 0o777
    expected_mode = 0o755
    assert (
        mode == expected_mode
    ), f"Directory {POLICY_DIR!s} should have permissions {oct(expected_mode)}, found {oct(mode)}"


def test_inventory_txt_exists_and_permissions():
    """
    inventory.txt must exist, be a regular file, and have mode 0644.
    """
    assert INVENTORY_TXT.exists(), f"Required file not found: {INVENTORY_TXT!s}"
    assert INVENTORY_TXT.is_file(), f"Expected a regular file at {INVENTORY_TXT!s}, but found something else."

    mode = INVENTORY_TXT.stat().st_mode & 0o777
    expected_mode = 0o644
    assert (
        mode == expected_mode
    ), f"File {INVENTORY_TXT!s} should have permissions {oct(expected_mode)}, found {oct(mode)}"


def test_inventory_txt_content_exact_match():
    """
    inventory.txt must contain exactly the five expected lines, in the correct order,
    and each line must match the <port>:<service>/<proto> pattern.  A single trailing
    newline must be present.
    """
    raw = INVENTORY_TXT.read_text(encoding="utf-8")

    # Verify a single trailing newline
    assert raw.endswith(
        "\n"
    ), f"{INVENTORY_TXT!s} must end with a single UNIX newline (\\n)."

    # Split without keeping the newline characters
    lines = raw.splitlines()

    # Ensure there are exactly five non-empty lines
    assert (
        len(lines) == 5
    ), f"{INVENTORY_TXT!s} must contain exactly 5 lines; found {len(lines)}."

    # Pattern conformity check
    bad_lines = [l for l in lines if LINE_REGEX.fullmatch(l) is None]
    assert (
        not bad_lines
    ), f"The following line(s) in {INVENTORY_TXT!s} do not match '<port>:<service>/<proto>': {bad_lines}"

    # Exact content check
    assert (
        lines == EXPECTED_LINES
    ), f"Contents of {INVENTORY_TXT!s} do not match the expected baseline.\nExpected: {EXPECTED_LINES}\nFound   : {lines}"