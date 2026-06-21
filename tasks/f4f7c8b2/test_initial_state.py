# test_initial_state.py
#
# This test-suite validates the **initial** filesystem state that must be
# present before the student’s automation script is executed.  It checks:
#
#   • required directories exist and have the correct permissions
#   • required data files exist, have the correct permissions and contain
#     the expected content
#   • /home/user/reports exists but is completely empty
#
# Only the Python standard library and pytest are used.

import os
import stat
import re
from pathlib import Path

DATA_DIR = Path("/home/user/data")
REPORTS_DIR = Path("/home/user/reports")

SERVERS_FILE   = DATA_DIR / "servers.cfg"
PORTS_FILE     = DATA_DIR / "ports.list"
PROVISION_FILE = DATA_DIR / "provision.log"


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def _perm_bits(path: Path) -> int:
    """Return UNIX permission bits as an int, e.g. 0o644."""
    return stat.S_IMODE(path.stat().st_mode)


def _assert_perm(path: Path, expected: int):
    actual = _perm_bits(path)
    assert actual == expected, (
        f"{path} must have permissions {oct(expected)}; "
        f"found {oct(actual)} instead."
    )


# --------------------------------------------------------------------------- #
# Directory checks
# --------------------------------------------------------------------------- #
def test_required_directories_exist_and_are_empty():
    # /home/user/data must exist, be a directory, and mode 755
    assert DATA_DIR.is_dir(), f"Expected directory {DATA_DIR} to exist."
    _assert_perm(DATA_DIR, 0o755)

    # /home/user/reports must exist, be a directory, and mode 755
    assert REPORTS_DIR.is_dir(), f"Expected directory {REPORTS_DIR} to exist."
    _assert_perm(REPORTS_DIR, 0o755)

    # /home/user/reports must be completely empty at the start
    contents = list(REPORTS_DIR.iterdir())
    assert not contents, (
        f"{REPORTS_DIR} should be empty before the student runs any code, "
        f"but it already contains: {[p.name for p in contents]}"
    )


# --------------------------------------------------------------------------- #
# /home/user/data/servers.cfg
# --------------------------------------------------------------------------- #
EXPECTED_SERVER_ENTRIES = [
    ("srv-alpha",   "active",   "10.10.1.11"),
    ("srv-beta",    "inactive", "10.10.1.12"),
    ("srv-gamma",   "active",   "10.10.1.13"),
    ("srv-delta",   "inactive", "10.10.1.14"),
    ("srv-epsilon", "active",   "10.10.1.15"),
]

SERVER_LINE_RE = re.compile(
    r"^server_id:(\S+)\s+status=(active|inactive)\s+ip=(\d+\.\d+\.\d+\.\d+)\s*$"
)


def test_servers_cfg_exists_correct_permissions_and_content():
    assert SERVERS_FILE.is_file(), f"Required file {SERVERS_FILE} is missing."
    _assert_perm(SERVERS_FILE, 0o644)

    lines = [ln.rstrip("\n") for ln in SERVERS_FILE.read_text().splitlines()]
    assert len(lines) == len(EXPECTED_SERVER_ENTRIES), (
        f"{SERVERS_FILE} should contain {len(EXPECTED_SERVER_ENTRIES)} lines, "
        f"found {len(lines)}."
    )

    active_count = inactive_count = 0
    for idx, (line, expected) in enumerate(zip(lines, EXPECTED_SERVER_ENTRIES), 1):
        m = SERVER_LINE_RE.match(line)
        assert m, (
            f"Line {idx} in {SERVERS_FILE} has unexpected format:\n--> {line}"
        )

        server_id, status, ip = m.groups()
        assert (server_id, status, ip) == expected, (
            f"Line {idx} in {SERVERS_FILE} differs from the expected entry.\n"
            f"Expected: {expected}\nFound:    {(server_id, status, ip)}"
        )

        if status == "active":
            active_count += 1
        else:
            inactive_count += 1

    # Sanity check on counts
    assert active_count == 3, f"Expected 3 active servers, found {active_count}."
    assert inactive_count == 2, f"Expected 2 inactive servers, found {inactive_count}."


# --------------------------------------------------------------------------- #
# /home/user/data/ports.list
# --------------------------------------------------------------------------- #
EXPECTED_PORTS = ["22", "80", "443", "8080", "8443", "3306", "5432"]


def test_ports_list_exists_correct_permissions_and_content():
    assert PORTS_FILE.is_file(), f"Required file {PORTS_FILE} is missing."
    _assert_perm(PORTS_FILE, 0o644)

    lines = [ln.rstrip("\n") for ln in PORTS_FILE.read_text().splitlines()]
    assert lines == EXPECTED_PORTS, (
        f"{PORTS_FILE} content mismatch.\n"
        f"Expected ports: {EXPECTED_PORTS}\nFound:          {lines}"
    )


# --------------------------------------------------------------------------- #
# /home/user/data/provision.log
# --------------------------------------------------------------------------- #
EXPECTED_LAST_PROVISION_LINE = (
    "2023-06-12T08:14:45Z Finished provisioning beta with error"
)
EXPECTED_PROVISION_LINE_COUNT = 6


def test_provision_log_exists_correct_permissions_and_content():
    assert PROVISION_FILE.is_file(), f"Required file {PROVISION_FILE} is missing."
    _assert_perm(PROVISION_FILE, 0o644)

    lines = [ln.rstrip("\n") for ln in PROVISION_FILE.read_text().splitlines()]
    assert len(lines) == EXPECTED_PROVISION_LINE_COUNT, (
        f"{PROVISION_FILE} should have {EXPECTED_PROVISION_LINE_COUNT} lines, "
        f"found {len(lines)}."
    )

    last_line = lines[-1].strip()
    assert last_line == EXPECTED_LAST_PROVISION_LINE, (
        f"The last line of {PROVISION_FILE} is not as expected.\n"
        f"Expected: {EXPECTED_LAST_PROVISION_LINE}\nFound:    {last_line}"
    )