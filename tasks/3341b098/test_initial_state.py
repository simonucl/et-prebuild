# test_initial_state.py
#
# This test-suite verifies that the *initial* filesystem state is exactly
# what the exercise description promises *before* the student starts
# working.  It intentionally avoids touching or asserting anything about
# the “output” area so that students may freely create those artefacts.
#
# Rules honoured:
#   • Uses only stdlib + pytest
#   • Checks absolute paths
#   • Does NOT test for any output files or directories
#   • Provides clear failure messages
#
# ---------------------------------------------------------------------------

from pathlib import Path
import os
import stat
import pytest

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

LOG_PATH = Path("/home/user/network/logs/conn.log")

# The exact, canonical contents that must be present in the handed-over log
EXPECTED_LOG_LINES = [
    '2023-09-14T23:58:12Z router=sfo-gw1 src=10.0.0.2 dst=8.8.8.8 proto=ICMP conn_status=OK latency=34ms',
    '2023-09-15T00:01:44Z router=nyc-core src=172.16.4.89 dst=1.1.1.1 proto=TCP conn_status=FAIL err=101 detail="SYN timeout"',
    '2023-09-15T00:02:53Z router=lon-edge src=192.168.1.4 dst=8.8.4.4 proto=UDP conn_status=OK',
    '2023-09-15T01:15:22Z router=nyc-core src=10.10.10.10 dst=142.250.72.238 proto=TCP conn_status=FAIL err=104 detail="RST received"',
    '2023-09-15T02:47:03Z router=sfo-gw1 src=10.0.0.3 dst=198.41.0.4 proto=UDP conn_status=FAIL err=108 detail="Port unreachable"',
    '2023-09-15T03:10:37Z router=lon-edge src=192.168.1.22 dst=8.8.8.8 proto=ICMP conn_status=FAIL err=101 detail="TTL exceeded"',
    '2023-09-15T04:21:12Z router=nyc-core src=172.16.5.5 dst=9.9.9.9 proto=TCP conn_status=FAIL err=104 detail="RST received"',
    '2023-09-15T04:45:44Z router=sfo-gw1 src=10.0.0.25 dst=8.8.4.4 proto=UDP conn_status=OK',
    '2023-09-15T05:33:19Z router=lon-edge src=192.168.1.42 dst=8.8.4.4 proto=UDP conn_status=FAIL err=108 detail="Timeout"',
    '2023-09-15T06:55:01Z router=nyc-core src=10.10.10.11 dst=142.250.72.238 proto=TCP conn_status=FAIL err=101 detail="SYN timeout"',
    '2023-09-15T08:00:00Z router=lon-edge src=192.168.1.45 dst=8.8.8.8 proto=ICMP conn_status=OK latency=37ms',
    '2023-09-15T09:09:09Z router=sfo-gw1 src=10.0.0.50 dst=198.41.0.4 proto=UDP conn_status=FAIL err=104 detail="Unknown"',
    '2023-09-15T10:10:10Z router=nyc-core src=172.16.5.6 dst=1.1.1.1 proto=TCP conn_status=FAIL err=108 detail="ECN failure"',
    '2023-09-15T11:11:11Z router=lon-edge src=192.168.1.46 dst=9.9.9.9 proto=UDP conn_status=OK',
    '2023-09-16T00:00:00Z router=sfo-gw1 src=10.0.0.2 dst=8.8.8.8 proto=ICMP conn_status=FAIL err=104 detail="Next-day test"',
]

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def _is_readable_regular_file(path: Path) -> bool:
    """True if *path* is an existing, regular file that the current user can read."""
    try:
        st = path.stat()
    except FileNotFoundError:
        return False
    return (
        stat.S_ISREG(st.st_mode)  # regular file
        and os.access(path, os.R_OK)
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_conn_log_present_and_readable():
    """The raw connection log must exist as a *readable* regular file."""
    assert _is_readable_regular_file(
        LOG_PATH
    ), f"Required log file missing or not readable: {LOG_PATH!s}"


def test_conn_log_contents_exact():
    """
    The handed-over log must contain the precise, canonical lines outlined in
    the task description.  Any deviation would indicate a corrupt or incomplete
    initial state.
    """
    with LOG_PATH.open(encoding="utf-8") as fh:
        actual_lines = fh.read().splitlines()

    assert actual_lines == EXPECTED_LOG_LINES, (
        "The contents of /home/user/network/logs/conn.log differ from the "
        "expected initial state.\n"
        "Hint: the file must be *exactly* as provided to the student."
    )