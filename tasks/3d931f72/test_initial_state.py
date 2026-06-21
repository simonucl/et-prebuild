# test_initial_state.py
#
# This test-suite validates ONLY the **initial** state of the workstation
# before the student starts working on the task “archive.test.lan DNS
# verification”.  It intentionally does NOT look for any of the artefacts
# that the student must later create (e.g. the reports directory or the
# dns_verification.log file).  Its sole responsibility is to make sure the
# indispensable input file is present, has the correct permissions, and
# contains the expected mapping for the hostname `archive.test.lan`.
#
# Requirements verified:
#   1. /home/user/build/infra/hosts_artifacts exists and is a regular file.
#   2. File permissions are 0644.
#   3. After stripping comment lines (those that begin with “#”),
#      a line exists that maps `archive.test.lan` to the IPv4 address
#      192.168.45.77, following classic /etc/hosts syntax.
#
# If any of these conditions are not met the tests will fail with an
# explicit, actionable error message.

import os
import stat
import pathlib
import ipaddress
import pytest

HOSTS_FILE = pathlib.Path("/home/user/build/infra/hosts_artifacts")
EXPECTED_IP = "192.168.45.77"
EXPECTED_HOSTNAME = "archive.test.lan"
EXPECTED_PERMS = 0o644


def _read_non_comment_lines(path: pathlib.Path):
    """
    Return a list of lines from *path* with comments (# …) stripped and
    leading/trailing whitespace removed. Blank lines are discarded.
    """
    with path.open("r", encoding="utf-8") as fp:
        return [
            line.strip()
            for line in fp
            if line.strip() and not line.lstrip().startswith("#")
        ]


def test_hosts_file_exists():
    assert HOSTS_FILE.exists(), (
        f"Required hosts override file not found: {HOSTS_FILE}\n"
        "Ensure the file is present at the exact path shown."
    )
    assert HOSTS_FILE.is_file(), (
        f"Expected {HOSTS_FILE} to be a regular file, "
        "but it appears to be missing or not a file."
    )


def test_hosts_file_permissions():
    actual_perms = stat.S_IMODE(HOSTS_FILE.stat().st_mode)
    assert actual_perms == EXPECTED_PERMS, (
        f"{HOSTS_FILE} must have permissions "
        f"{oct(EXPECTED_PERMS)} but has {oct(actual_perms)}. "
        "Fix the permissions to be world-readable regular file (0644)."
    )


def test_hosts_file_contains_correct_mapping():
    """
    Verify that the hosts file contains exactly one line mapping
    archive.test.lan to 192.168.45.77 (aliases are allowed but the primary
    hostname must be present immediately after the IP).
    """
    lines = _read_non_comment_lines(HOSTS_FILE)

    matches = []
    for ln in lines:
        # Split on whitespace, ignore multiple spaces/tabs
        parts = ln.split()
        if len(parts) < 2:
            continue  # malformed, but not our concern here
        ip, primary_host, *aliases = parts

        # Quick sanity check that the first token is a valid IPv4 address.
        try:
            ipaddress.IPv4Address(ip)
        except ipaddress.AddressValueError:
            continue  # skip, not a valid IPv4 address in first field

        if primary_host == EXPECTED_HOSTNAME:
            matches.append((ip, ln))

    assert matches, (
        f"No non-comment line found in {HOSTS_FILE} where the primary "
        f"hostname is exactly '{EXPECTED_HOSTNAME}'.\n"
        "Every active line must follow: <IPv4> <primary-hostname> [aliases...]"
    )

    # There should be exactly one mapping; multiple would be ambiguous.
    assert len(matches) == 1, (
        f"Found multiple ({len(matches)}) mappings for {EXPECTED_HOSTNAME} "
        f"in {HOSTS_FILE}. There should be exactly one."
    )

    found_ip, _line = matches[0]
    assert found_ip == EXPECTED_IP, (
        f"{HOSTS_FILE} maps {EXPECTED_HOSTNAME} to {found_ip}, "
        f"but expected {EXPECTED_IP}. Update the file accordingly."
    )