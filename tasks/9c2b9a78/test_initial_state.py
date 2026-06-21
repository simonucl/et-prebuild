# test_initial_state.py
"""
Pytest suite validating the initial state of the filesystem *before* the student
runs any command.

Checks performed:
1. /home/user/servers.log exists and is a regular file.
2. The file contains exactly 7 non-empty lines.
3. Every line matches the expected CSV schema:
       server_id,status,uptime_days,load_average
   where:
       - server_id  : 'srv' followed by exactly two digits
       - status     : one of OK, DOWN, WARNING
       - uptime_days: integer >= 0
       - load_avg   : floating point number with exactly two decimals
4. Exactly three lines have the status field equal to 'DOWN'.

NOTE: The tests do *not* look for /home/user/down_count.log, because that file
      should not exist yet.  They only validate the pre-task state.
"""

from pathlib import Path
import re
import pytest

SERVERS_LOG = Path("/home/user/servers.log")

LINE_PATTERN = re.compile(
    r"^srv\d{2},"
    r"(OK|DOWN|WARNING),"
    r"\d+,"               # uptime_days
    r"\d+\.\d{2}$"        # load_average with exactly two decimals
)

@pytest.fixture(scope="module")
def server_lines():
    """Return a list of stripped, non-empty lines from servers.log."""
    if not SERVERS_LOG.exists():
        pytest.fail(f"Required file {SERVERS_LOG} is missing.")
    if not SERVERS_LOG.is_file():
        pytest.fail(f"Expected {SERVERS_LOG} to be a regular file, but it is not.")

    try:
        content = SERVERS_LOG.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Could not read {SERVERS_LOG}: {exc}")

    # Splitlines keeps content agnostic to trailing newline presence.
    lines = [ln.strip() for ln in content.splitlines() if ln.strip()]

    return lines


def test_line_count(server_lines):
    """Ensure the file has exactly 7 non-empty lines."""
    assert len(server_lines) == 7, (
        f"{SERVERS_LOG} should contain exactly 7 non-empty lines but has "
        f"{len(server_lines)}."
    )


def test_line_format(server_lines):
    """Each line must match the required CSV schema."""
    for idx, line in enumerate(server_lines, start=1):
        assert LINE_PATTERN.match(line) is not None, (
            f"Line {idx} in {SERVERS_LOG} is malformed: '{line}'.\n"
            "Expected pattern: 'srvXY,STATUS,UPTIME_DAYS,LOAD.AVG' where "
            "STATUS is one of OK, DOWN, WARNING and LOAD.AVG has two decimals."
        )


def test_down_count(server_lines):
    """Verify there are exactly 3 lines with status 'DOWN'."""
    down_lines = [ln for ln in server_lines if ",DOWN," in ln]
    assert len(down_lines) == 3, (
        f"Expected exactly 3 servers in DOWN state, found {len(down_lines)}.\n"
        f"Lines with status DOWN: {down_lines}"
    )