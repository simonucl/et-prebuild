# test_initial_state.py
#
# This test-suite validates that the *initial* filesystem state is exactly as
# expected *before* the student performs any action.  We explicitly verify only
# the presence and the correctness of the **input** artefacts.  We do **not**
# look for (or against) any of the files/directories that the student is asked
# to create later on.

import pathlib
import pytest

# Fixed, known paths
HOME = pathlib.Path("/home/user")
LOGS_DIR = HOME / "logs"
RESOURCES_DIR = HOME / "resources"

DNS_FAILURES_LOG = LOGS_DIR / "dns_failures.log"
HOSTS_OVERRIDE   = RESOURCES_DIR / "hosts_override"


# --------------------------------------------------------------------------- #
# Reference data ‑- the truth asserted by the task description
# --------------------------------------------------------------------------- #
EXPECTED_HOSTNAMES_ORDER = [
    "app.internal.local",
    "db.internal.local",
    "cache.internal.local",
    "auth.service",
    "gateway.service",
]

# Mapping of hostnames to expected IPv4s *only* for those that must resolve
EXPECTED_OVERRIDES = {
    "app.internal.local":   "10.0.0.11",
    "db.internal.local":    "10.0.0.12",
    "cache.internal.local": "10.0.0.13",
}


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def read_file_lines(path: pathlib.Path):
    """
    Return a list of *stripped* lines (without trailing LF/CR) for a text file.
    Raises an AssertionError if the file is unreadable.
    """
    try:
        with path.open(encoding="utf-8") as fh:
            return [line.rstrip("\r\n") for line in fh]
    except FileNotFoundError:
        pytest.fail(f"Required file is missing: {path!s}")
    except PermissionError:
        pytest.fail(f"Required file is not readable by current user: {path!s}")


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_logs_directory_exists():
    assert LOGS_DIR.is_dir(), (
        f"Expected logs directory does not exist at {LOGS_DIR!s}"
    )

def test_resources_directory_exists():
    assert RESOURCES_DIR.is_dir(), (
        f"Expected resources directory does not exist at {RESOURCES_DIR!s}"
    )

def test_dns_failures_log_content():
    lines = read_file_lines(DNS_FAILURES_LOG)
    assert lines, f"{DNS_FAILURES_LOG!s} is empty—expected a list of hostnames."

    # Ensure exact order and content
    assert lines == EXPECTED_HOSTNAMES_ORDER, (
        f"{DNS_FAILURES_LOG!s} does not contain the expected hostnames/ordering.\n"
        f"Expected: {EXPECTED_HOSTNAMES_ORDER}\nFound:    {lines}"
    )

def test_hosts_override_content():
    lines = read_file_lines(HOSTS_OVERRIDE)
    assert lines, f"{HOSTS_OVERRIDE!s} is empty—expected IPv4/hostname mappings."

    # Build mapping from the file
    mapping = {}
    for lineno, line in enumerate(lines, 1):
        # Each line must have exactly two fields separated by a *single* space.
        parts = line.split(" ")
        assert len(parts) == 2, (
            f"{HOSTS_OVERRIDE!s}, line {lineno}: expected exactly two "
            f"space-separated fields <IPv4> <hostname>; found: {line!r}"
        )
        ip, host = parts
        mapping[host] = ip

    # Ensure every expected override is present and correct.
    for host, ip in EXPECTED_OVERRIDES.items():
        assert host in mapping, (
            f"{HOSTS_OVERRIDE!s} is missing an entry for hostname: {host}"
        )
        assert mapping[host] == ip, (
            f"{HOSTS_OVERRIDE!s} has incorrect IPv4 for {host}. "
            f"Expected {ip}, found {mapping[host]}"
        )

    # Optionally verify there are no unexpected duplicates
    assert len(mapping) == len(set(mapping)), (
        f"{HOSTS_OVERRIDE!s} contains duplicate hostname entries."
    )