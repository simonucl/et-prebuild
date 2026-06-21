# test_initial_state.py
#
# Pytest suite that verifies the OS / filesystem state *before* the student
# performs any actions for the “dns_profile.log” assignment.
#
# The tests assert that only the two helper files are present and that their
# contents exactly match the specification.  They also confirm that the
# output file (`/home/user/profiling/dns_profile.log`) does **not** yet exist.
#
# If any assertion fails, the error message will clearly indicate what is
# missing or malformed so the student can correct the initial setup.

import os
from pathlib import Path
import pytest

# Base directory used throughout the assignment.
BASE_DIR = Path("/home/user/profiling")

HOST_TARGETS = BASE_DIR / "host_targets.txt"
IP_MAP       = BASE_DIR / "ip_map.txt"
DNS_PROFILE  = BASE_DIR / "dns_profile.log"

# Expected canonical data ----------------------------------------------------

EXPECTED_HOSTNAMES = [
    "frontend.local",
    "backend.local",
    "db.local",
]

EXPECTED_IP_MAP_LINES = [
    "192.168.50.10 frontend.local",
    "192.168.50.20 backend.local",
    "192.168.50.30 db.local",
]


# Helper functions -----------------------------------------------------------

def _read_file_lines(path: Path):
    """
    Return a list of strings representing the lines in *path* with the trailing
    newline removed **without** stripping any other whitespace.  This allows us
    to check for accidental leading/trailing spaces inside each line.
    """
    with path.open("r", encoding="utf-8") as fh:
        return [ln.rstrip("\n") for ln in fh.readlines()]


# Tests ----------------------------------------------------------------------

def test_profiling_directory_exists():
    assert BASE_DIR.is_dir(), (
        f"Required directory {BASE_DIR} is missing.  Expected the helper files "
        "to be located there."
    )


@pytest.mark.parametrize("required_file", [HOST_TARGETS, IP_MAP])
def test_helper_files_exist(required_file: Path):
    assert required_file.is_file(), (
        f"Required file {required_file} is missing.  Make sure it exists at the "
        "specified absolute path."
    )


def test_host_targets_content():
    lines = _read_file_lines(HOST_TARGETS)

    assert lines == EXPECTED_HOSTNAMES, (
        f"{HOST_TARGETS} has unexpected content.\n"
        f"Expected lines (in order): {EXPECTED_HOSTNAMES}\n"
        f"Actual lines           : {lines}"
    )

    # Verify the file ends with a single Unix newline.
    with HOST_TARGETS.open("rb") as fh:
        fh.seek(-1, os.SEEK_END)
        last_byte = fh.read(1)
    assert last_byte == b"\n", (
        f"{HOST_TARGETS} must end with a single newline character (\\n)."
    )


def test_ip_map_content():
    lines = _read_file_lines(IP_MAP)

    assert lines == EXPECTED_IP_MAP_LINES, (
        f"{IP_MAP} has unexpected content.\n"
        f"Expected lines (in order): {EXPECTED_IP_MAP_LINES}\n"
        f"Actual lines           : {lines}"
    )

    for idx, line in enumerate(lines, start=1):
        # Ensure exactly one space separates IP and hostname.
        parts = line.split(" ")
        assert len(parts) == 2, (
            f"Line {idx} in {IP_MAP!s} should contain exactly two columns "
            f"separated by a single space.\nFound: {line!r}"
        )
        ip, host = parts
        assert host == EXPECTED_HOSTNAMES[idx - 1], (
            f"Hostname mismatch on line {idx} of {IP_MAP}: "
            f"expected '{EXPECTED_HOSTNAMES[idx - 1]}', got '{host}'."
        )

    # Verify the file ends with a single Unix newline.
    with IP_MAP.open("rb") as fh:
        fh.seek(-1, os.SEEK_END)
        last_byte = fh.read(1)
    assert last_byte == b"\n", (
        f"{IP_MAP} must end with a single newline character (\\n)."
    )


def test_output_file_not_present_yet():
    assert not DNS_PROFILE.exists(), (
        f"Output file {DNS_PROFILE} already exists, but the tests are run on "
        "the initial state.  Please remove it before starting the assignment."
    )