# test_initial_state.py
#
# This pytest suite validates that the starting filesystem state is
# correct *before* the student performs any action.
#
# What we assert:
#   1. The directory /home/user/provision exists.
#   2. The files servers.dat and ips.dat exist inside that directory
#      and contain the exact, byte-for-byte contents described in
#      the task (single LF line endings, no CR characters).
#   3. The file inventory.txt must *not* exist yet.
#
# If any of these conditions fail, the test will raise a clear,
# descriptive assertion error explaining what is missing or wrong.
#
# Only the Python standard library and pytest are used.

import os
from pathlib import Path

import pytest

PROVISION_DIR = Path("/home/user/provision")
SERVERS_DAT = PROVISION_DIR / "servers.dat"
IPS_DAT = PROVISION_DIR / "ips.dat"
INVENTORY_TXT = PROVISION_DIR / "inventory.txt"

# Expected exact byte contents (LF endings, no trailing blank line)
EXPECTED_SERVERS_CONTENT = (
    "hostname,role,dc\n"
    "web01,app,dc1\n"
    "db01,db,dc1\n"
    "cache01,cache,dc2\n"
).encode()

EXPECTED_IPS_CONTENT = (
    "ip,netmask\n"
    "10.0.0.11,255.255.255.0\n"
    "10.0.0.21,255.255.255.0\n"
    "10.0.0.31,255.255.255.0\n"
).encode()


def _read_bytes(path: Path) -> bytes:
    """Read a file as raw bytes, returning empty bytes if it does not exist."""
    with path.open("rb") as fh:
        return fh.read()


def test_provision_directory_exists():
    assert PROVISION_DIR.is_dir(), (
        f"Required directory {PROVISION_DIR} is missing. "
        "Create it before continuing."
    )


@pytest.mark.parametrize(
    ("path", "expected"),
    [
        (SERVERS_DAT, EXPECTED_SERVERS_CONTENT),
        (IPS_DAT, EXPECTED_IPS_CONTENT),
    ],
)
def test_dat_files_exist_with_exact_contents(path: Path, expected: bytes):
    assert path.is_file(), f"Expected file {path} is missing."
    actual = _read_bytes(path)

    # 1. Ensure pure LF endings (no CR characters)
    assert b"\r" not in actual, (
        f"{path} contains CR (\\r) characters; "
        "use pure LF line endings."
    )

    # 2. Ensure the file ends with a single LF but not two
    assert actual.endswith(b"\n"), f"{path} must end with a single newline (LF)."
    assert not actual.endswith(b"\n\n"), (
        f"{path} has more than one trailing blank line."
    )

    # 3. Ensure the full content is exactly as expected
    assert actual == expected, (
        f"Contents of {path} do not match the expected initial state.\n"
        "---- Expected ----\n"
        f"{expected.decode()}"
        "----   Got   ----\n"
        f"{actual.decode()}"
        "------------------"
    )

def test_inventory_txt_absent_initially():
    assert not INVENTORY_TXT.exists(), (
        f"{INVENTORY_TXT} should NOT exist yet. "
        "Create it only after processing the .dat files."
    )