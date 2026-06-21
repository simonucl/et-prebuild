# test_initial_state.py
#
# Pytest suite that validates the **initial** operating‐system / filesystem
# state for the “DNS allow-list audit” exercise.
#
# What we verify:
# 1. Directory /home/user/policy exists.
# 2. File /home/user/policy/dns_allowlist.txt exists, is regular, is world-readable
#    (mode 0644), and has exactly the two expected hostnames in order:
#       - localhost
#       - invalid.local
# 3. File /home/user/policy/dns_audit.csv does *not* yet exist.
# 4. System DNS behaviour matches the exercise’s ground truth:
#       - “localhost” resolves to at least one IPv4 address, the first of which
#         must be 127.0.0.1.
#       - “invalid.local” cannot be resolved at all.
#
# These assertions guarantee that students start from the correct baseline
# before implementing their solution.

import os
import stat
import socket
from pathlib import Path

import pytest

POLICY_DIR = Path("/home/user/policy")
ALLOWLIST_FILE = POLICY_DIR / "dns_allowlist.txt"
AUDIT_CSV_FILE = POLICY_DIR / "dns_audit.csv"


def test_policy_directory_exists():
    assert POLICY_DIR.is_dir(), (
        f"Required directory {POLICY_DIR} is missing. "
        "Create it or adjust the file paths accordingly."
    )


def test_allowlist_file_properties_and_contents():
    # Existence & type
    assert ALLOWLIST_FILE.is_file(), (
        f"Allow-list file {ALLOWLIST_FILE} is missing."
    )

    # Permissions: world-readable, no executable bits (octal 0644)
    st_mode = ALLOWLIST_FILE.stat().st_mode
    actual_perms = stat.S_IMODE(st_mode)
    expected_perms = 0o644
    assert actual_perms == expected_perms, (
        f"{ALLOWLIST_FILE} permissions are {oct(actual_perms)}, "
        f"expected {oct(expected_perms)} (rw-r--r--)."
    )

    # Exact contents
    with ALLOWLIST_FILE.open("r", encoding="utf-8") as fh:
        raw = fh.read()

    # Preserve possible trailing newline for a robust comparison
    lines = raw.splitlines()

    expected_lines = ["localhost", "invalid.local"]
    assert lines == expected_lines, (
        f"Contents of {ALLOWLIST_FILE} differ from the specification.\n"
        f"Expected lines: {expected_lines!r}\n"
        f"Actual lines  : {lines!r}"
    )


def test_audit_csv_does_not_exist_yet():
    assert not AUDIT_CSV_FILE.exists(), (
        f"The compliance report {AUDIT_CSV_FILE} already exists, "
        "but the student has not yet been asked to create it. "
        "Remove or rename this file before starting the task."
    )


def test_dns_resolution_ground_truth():
    """
    Confirm that the local resolver behaves exactly as the exercise expects:
    - 'localhost' resolves to 127.0.0.1 (first IPv4 address)
    - 'invalid.local' is unresolvable
    """
    # localhost must resolve
    try:
        localhost_ips = socket.gethostbyname_ex("localhost")[2]
    except socket.gaierror as exc:  # pragma: no cover
        pytest.fail(f"'localhost' failed to resolve: {exc}")

    assert localhost_ips, "'localhost' resolved but returned no IP addresses."
    assert localhost_ips[0] == "127.0.0.1", (
        f"'localhost' first IPv4 is {localhost_ips[0]!r}, "
        "expected '127.0.0.1'."
    )

    # invalid.local must not resolve
    with pytest.raises(socket.gaierror):
        socket.gethostbyname("invalid.local")