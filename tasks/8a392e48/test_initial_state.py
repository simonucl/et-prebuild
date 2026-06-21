# test_initial_state.py
#
# This test-suite verifies the *initial* state of the operating-system
# before the student performs any action for the “DNS sanity-check”
# exercise.  The environment must be clean: no pre-existing “release”
# directory nor the target log file must be present, while the system
# resolver must already map “localhost” to “127.0.0.1”.
#
# All checks use absolute paths and rely solely on the Python stdlib
# plus pytest.

import os
import socket
from pathlib import Path

import pytest

HOME = Path("/home/user").resolve()
RELEASE_DIR = HOME / "release"
LOG_FILE = RELEASE_DIR / "dns_precheck.log"


def _localhost_ipv4_addresses():
    """
    Return a set of all IPv4 addresses that the local resolver
    associates with the hostname 'localhost'.
    """
    results = set()
    # socket.getaddrinfo returns 5-tuples; the [4][0] item is the IP.
    for family, _, _, _, sockaddr in socket.getaddrinfo("localhost", None):
        if family == socket.AF_INET:  # IPv4 only
            results.add(sockaddr[0])
    return results


def test_home_directory_exists_and_is_directory():
    assert HOME.exists(), (
        f"Expected home directory {HOME} to exist, "
        "but it is missing. The test environment is not set up correctly."
    )
    assert HOME.is_dir(), f"{HOME} exists but is not a directory."


def test_release_directory_does_not_yet_exist():
    assert not RELEASE_DIR.exists(), (
        f"Found unexpected path {RELEASE_DIR}. "
        "The 'release' directory must NOT exist before the student runs their solution."
    )


def test_dns_precheck_log_does_not_yet_exist():
    assert not LOG_FILE.exists(), (
        f"Found unexpected file {LOG_FILE}. "
        "The dns_precheck.log file must NOT be present before the student creates it."
    )


def test_localhost_resolves_to_127_0_0_1():
    ipv4_set = _localhost_ipv4_addresses()
    assert ipv4_set, (
        "The hostname 'localhost' did not return any IPv4 addresses. "
        "A minimal Linux installation should map 'localhost' to 127.0.0.1."
    )
    assert "127.0.0.1" in ipv4_set, (
        "'localhost' does not resolve to 127.0.0.1 on this machine. "
        f"Addresses returned: {', '.join(sorted(ipv4_set))}"
    )