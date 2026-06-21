# test_initial_state.py
#
# This test-suite validates that the *initial* environment has the
# basic tools and connectivity required **before** the student creates
# /home/user/migration_diagnostics/report.log.
#
# NOTE:
# • We intentionally DO NOT reference the output directory or file
#   ( /home/user/migration_diagnostics/report.log ) because that path
#   will be created by the student during the exercise.
# • Only the Python stdlib and pytest are used.

import os
import shutil
import socket
import pytest
import re

HOME_DIR = "/home/user"
TEST_HOST = "example.com"


def _cmd_exists(cmd_name: str) -> bool:
    """
    Return True if an executable command exists in PATH.
    """
    return shutil.which(cmd_name) is not None


def _get_ipv4_addresses(hostname: str):
    """
    Resolve hostname and return a set of IPv4 addresses (strings).
    """
    try:
        addr_info = socket.getaddrinfo(hostname, None, family=socket.AF_INET)
    except socket.gaierror as exc:
        raise RuntimeError(
            f"DNS lookup for '{hostname}' failed: {exc}. "
            "The system must be able to resolve this hostname."
        ) from exc

    return {entry[4][0] for entry in addr_info}


# ----------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------

def test_home_directory_exists():
    assert os.path.isdir(
        HOME_DIR
    ), f"Expected home directory '{HOME_DIR}' to exist and be a directory."


@pytest.mark.parametrize(
    "candidates,description",
    [
        (("dig", "nslookup"), "DNS lookup utility (dig or nslookup)"),
        (("ping",), "ICMP ping utility (ping)"),
        (("curl", "wget"), "HTTP client utility (curl or wget)"),
    ],
)
def test_required_cli_tools_present(candidates, description):
    available = [cmd for cmd in candidates if _cmd_exists(cmd)]
    assert (
        available
    ), f"None of the required commands {candidates} were found for: {description}."


def test_dns_resolves_example_com_to_ipv4():
    ipv4_set = _get_ipv4_addresses(TEST_HOST)
    human_readable = ", ".join(sorted(ipv4_set)) or "<none>"

    # Validate we got at least one IPv4 address that matches an IPv4 regex.
    ip_regex = re.compile(r"^(\d{1,3}\.){3}\d{1,3}$")
    bad_ips = [ip for ip in ipv4_set if not ip_regex.match(ip)]
    assert ipv4_set, f"DNS lookup returned no IPv4 addresses for {TEST_HOST}."
    assert (
        not bad_ips
    ), f"The following resolved IPs do not appear to be valid IPv4 addresses: {bad_ips}"
    # Additional helpful context if assertion passes but someone looks at test output
    print(f"[info] {TEST_HOST} resolved to: {human_readable}")