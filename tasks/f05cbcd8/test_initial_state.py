# test_initial_state.py
#
# This test-suite validates that the sandbox starts from the **expected,
# unmodified state** before the student begins any work on the DNS incident
# exercise.  It intentionally makes **no assertions** about any files that
# must be generated or altered by the student solution.

import json
import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
TICKET_FILE = HOME / "incidents" / "tickets" / "dns_incident_2024.txt"
MOCK_HOSTS = HOME / "resources" / "mock_hosts"
MOCK_DNS = HOME / "resources" / "mock_dns_records.json"

# ---------------------------------------------------------------------------#
# Helper functions
# ---------------------------------------------------------------------------#
def read_nonblank_lines(path: Path):
    """Return a list of lines stripped of the trailing newline, excluding blank
    lines.  Keep original ordering."""
    with path.open("r", encoding="utf-8") as fh:
        return [ln.rstrip("\n") for ln in fh if ln.strip()]


def hosts_file_mapping(path: Path):
    """
    Parse a hosts-style file and return an ordered list of tuples
    (ip_address, hostname) for every non-blank, non-comment line.
    Only the first two whitespace-separated fields are considered.
    """
    mapping = []
    for raw in read_nonblank_lines(path):
        # Discard comments *after* stripping trailing spaces to keep order.
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) < 2:
            continue  # malformed, ignore here – test will fail later
        mapping.append((parts[0], parts[1]))
    return mapping


# ---------------------------------------------------------------------------#
# Tests
# ---------------------------------------------------------------------------#
def test_required_files_exist():
    """All input artefacts must be present and be regular files."""
    for path in (TICKET_FILE, MOCK_HOSTS, MOCK_DNS):
        assert path.exists(), f"Expected file {path} is missing."
        assert path.is_file(), f"{path} exists but is not a regular file."


def test_ticket_file_contents():
    """The ticket file must list exactly the three hostnames, one per line."""
    expected = ["app.web.internal", "example.com", "localhost"]
    actual = read_nonblank_lines(TICKET_FILE)
    assert (
        actual == expected
    ), f"Unexpected ticket contents.\nExpected lines: {expected!r}\nActual lines:   {actual!r}"


def test_mock_hosts_initial_state():
    """mock_hosts must start with precisely the three expected mappings and
    nothing else."""
    expected_ordered = [
        ("127.0.0.1", "localhost"),
        ("::1", "localhost"),
        ("10.0.0.5", "app.web.internal"),
    ]
    actual = hosts_file_mapping(MOCK_HOSTS)

    # 1) Check that we have exactly three entries
    assert (
        len(actual) == len(expected_ordered)
    ), f"mock_hosts should contain {len(expected_ordered)} entries but has {len(actual)} entries: {actual}"

    # 2) Check order and content
    for (exp_ip, exp_host), (act_ip, act_host) in zip(expected_ordered, actual):
        assert (
            exp_ip == act_ip and exp_host == act_host
        ), f"mock_hosts line mismatch.\nExpected: {(exp_ip, exp_host)}\nActual:   {(act_ip, act_host)}"

    # 3) Ensure example.com is NOT present yet
    assert not any(
        host == "example.com" for _, host in actual
    ), "example.com must NOT be present in the initial mock_hosts file."


def test_mock_dns_records_json():
    """Validate the deterministic JSON DNS data."""
    with MOCK_DNS.open("r", encoding="utf-8") as fh:
        data = json.load(fh)

    # Exact expected structure
    expected = {
        "app.web.internal": {"A": "", "AAAA": ""},
        "example.com": {
            "A": "93.184.216.34",
            "AAAA": "2606:2800:220:1:248:1893:25c8:1946",
        },
        "localhost": {"A": "127.0.0.1", "AAAA": "::1"},
    }

    assert (
        data == expected
    ), f"mock_dns_records.json differs from the expected contents.\nExpected: {json.dumps(expected, indent=2)}\nActual:   {json.dumps(data, indent=2)}"


def test_file_permissions():
    """All provided files should be readable/writable by the student and NOT
    world-writable."""
    for path in (TICKET_FILE, MOCK_HOSTS, MOCK_DNS):
        mode = path.stat().st_mode & 0o777  # only permission bits
        assert mode & 0o200, f"{path} must be writable by owner."
        assert mode & 0o400, f"{path} must be readable by owner."
        assert not (
            mode & 0o002
        ), f"{path} must not be world-writable (expected 0640/0660 style permissions)."