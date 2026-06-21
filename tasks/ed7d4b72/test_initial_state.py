# test_initial_state.py
#
# Pytest suite that validates the operating system / filesystem *before*
# the student performs any actions for the “network backup” exercise.
#
# What we verify (ONLY pre-existing state, never the deliverables):
#   1. /home/user/net_logs/ exists and is a directory.
#   2. /home/user/net_logs/ping_output.txt exists and has the expected
#      two-line contents (including trailing newlines).
#   3. /home/user/net_logs/traceroute_output.txt exists and has the
#      expected three-line contents (including trailing newlines).
#
# We intentionally do *not* check for /home/user/archives or anything
# inside it, because that directory is part of the student’s required
# output and must not be asserted in the initial-state test.

import os
from pathlib import Path

import pytest

NET_LOGS_DIR = Path("/home/user/net_logs")
PING_FILE = NET_LOGS_DIR / "ping_output.txt"
TRACEROUTE_FILE = NET_LOGS_DIR / "traceroute_output.txt"


@pytest.mark.parametrize(
    "path",
    [NET_LOGS_DIR, PING_FILE, TRACEROUTE_FILE],
)
def test_required_paths_exist(path: Path):
    """
    Ensure the directory and both log files are present before any
    student action is performed.
    """
    assert path.exists(), f"Required path missing: {path}"
    if path is NET_LOGS_DIR:
        assert path.is_dir(), f"{NET_LOGS_DIR} should be a directory"
    else:
        assert path.is_file(), f"{path} should be a regular file"


def test_ping_output_contents():
    """
    Verify the exact, two-line contents of ping_output.txt (including
    trailing newlines).
    """
    expected_lines = [
        "PING 8.8.8.8 (8.8.8.8): 56 data bytes\n",
        "64 bytes from 8.8.8.8: icmp_seq=0 ttl=115 time=12.3 ms\n",
    ]

    with PING_FILE.open("r", encoding="utf-8") as fh:
        actual_lines = fh.readlines()

    assert (
        actual_lines == expected_lines
    ), f"{PING_FILE} contents differ from the expected initial state"


def test_traceroute_output_contents():
    """
    Verify the exact, three-line contents of traceroute_output.txt
    (including trailing newlines).
    """
    expected_lines = [
        "traceroute to 8.8.8.8 (8.8.8.8), 30 hops max\n",
        " 1  10.0.0.1 (10.0.0.1)  1.123 ms\n",
        " 2  8.8.8.8 (8.8.8.8)  12.345 ms\n",
    ]

    with TRACEROUTE_FILE.open("r", encoding="utf-8") as fh:
        actual_lines = fh.readlines()

    assert (
        actual_lines == expected_lines
    ), f"{TRACEROUTE_FILE} contents differ from the expected initial state"