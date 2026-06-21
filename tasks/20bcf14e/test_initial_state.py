# test_initial_state.py
#
# Pytest suite to validate the **initial** state of the system
# before the student performs any action for the DNS-resolution
# incident-response exercise.

import os
import stat
import socket
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def ipv4_addresses(hostname: str) -> list[str]:
    """
    Return a list of IPv4 addresses for *hostname* using the system resolver.
    If the lookup fails (or yields only non-IPv4 results), an empty list
    is returned.
    """
    try:
        results = socket.getaddrinfo(hostname, None, socket.AF_INET)
    except socket.gaierror:
        return []

    addresses: list[str] = []
    for family, _socktype, _proto, _canonname, sockaddr in results:
        if family == socket.AF_INET:
            ip, *_ = sockaddr
            addresses.append(ip)
    return addresses


# --------------------------------------------------------------------------- #
# Filesystem sanity checks
# --------------------------------------------------------------------------- #
IR_DIR = Path("/home/user/ir")
IR_LOG = IR_DIR / "dns_resolution.log"


def test_ir_directory_may_exist_but_log_must_not(tmp_path_factory):
    """
    Prior to the student's work, the directory /home/user/ir might or might
    not exist.  In **either** case, the DNS log file MUST NOT already be
    present.  This guarantees that the assessment starts from a clean slate.
    """
    assert (
        not IR_LOG.exists()
    ), (
        f"The file {IR_LOG} already exists, but it should NOT be present before "
        "the student carries out the task."
    )

    if IR_DIR.exists():
        # If the directory already exists, ensure it is a directory (not a
        # symlink, device, etc.) and that it is writable by the user who is
        # going to create the log later.
        assert IR_DIR.is_dir(), f"{IR_DIR} exists but is not a directory."
        mode = IR_DIR.stat().st_mode
        # The dir must at least be user-writable (0700 or 0755 etc.).
        assert mode & stat.S_IWUSR, (
            f"The directory {IR_DIR} exists but is not writable by the user."
        )


# --------------------------------------------------------------------------- #
# DNS-resolution baseline checks
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "hostname, should_resolve, expected_first_ip",
    [
        ("localhost", True, "127.0.0.1"),
        ("metadata.google.internal", False, None),
        ("definitely-not-real.tld", False, None),
    ],
)
def test_dns_baseline(hostname, should_resolve, expected_first_ip):
    """
    Validate that the system resolver behaves exactly as the exercise
    description states *before* the student touches anything.

    localhost                   -> must resolve to 127.0.0.1
    metadata.google.internal    -> must NOT resolve (in this sandbox)
    definitely-not-real.tld     -> must NOT resolve
    """
    addrs = ipv4_addresses(hostname)

    if should_resolve:
        assert (
            addrs
        ), f"Expected {hostname} to resolve, but it did not return any IPv4 address."
        assert (
            expected_first_ip in addrs
        ), (
            f"{hostname} resolved, but  {expected_first_ip!r} was not among the IPv4 "
            f"addresses returned: {addrs}"
        )
    else:
        assert (
            not addrs
        ), f"Expected {hostname} to fail resolution, but got IPv4 addresses: {addrs}"