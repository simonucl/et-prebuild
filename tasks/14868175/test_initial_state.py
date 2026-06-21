# test_initial_state.py
#
# Pytest suite that verifies the *initial* operating-system / filesystem
# state **before** the student performs any actions for the “ICMP statistics
# to CSV” assignment.
#
# The tests deliberately check only pre-existing artefacts and never look
# for (or forbid) the output file that the student will eventually create.
#
# Usage:
#   pytest -q                                   # should pass on the clean VM


import os
import re
from pathlib import Path

NETWORK_DIR = Path("/home/user/network")
PING_RESULTS = NETWORK_DIR / "ping_results.txt"


def test_network_directory_exists():
    """
    The /home/user/network directory must already be present so that the
    student can place the resulting CSV next to the raw capture.
    """
    assert NETWORK_DIR.is_dir(), (
        f"Required directory {NETWORK_DIR} is missing. "
        "Create it before running the assignment."
    )


def test_ping_results_file_exists():
    """
    The raw ICMP capture must exist at the exact, absolute path stated in
    the specification.
    """
    assert PING_RESULTS.is_file(), (
        f"Input file {PING_RESULTS} is missing. "
        "Ensure the technician's capture has been copied to the workstation."
    )


def _get_stats_blocks(text):
    """
    Extract all 'ping statistics' blocks (one per host) from the file.

    A block starts with:
        --- <IP> ping statistics ---
    and includes (at minimum) the immediately following line that contains
    '<n> packets transmitted'.
    """
    pattern = re.compile(
        r"^---\s+(?P<ip>[\d\.]+)\s+ping statistics\s+---\s*$\n"
        r"^(?P<stats_line>.+packets transmitted.+)$",
        re.MULTILINE,
    )
    return pattern.findall(text)


def test_ping_results_contains_three_hosts_with_stats():
    """
    Validate that the capture includes exactly three statistics sections
    (one for each host) and that each section follows the expected pattern.
    """
    text = PING_RESULTS.read_text(encoding="utf-8", errors="replace")

    stats_blocks = _get_stats_blocks(text)

    # We expect exactly three hosts in the initial fixture.
    expected_hosts = {"192.168.1.1", "10.0.0.1", "172.16.0.1"}
    found_hosts = {ip for ip, _ in stats_blocks}

    assert len(stats_blocks) == 3, (
        "The input file should contain statistics for exactly three hosts "
        f"({', '.join(sorted(expected_hosts))}). "
        f"Found {len(stats_blocks)} section(s) instead."
    )

    missing = expected_hosts - found_hosts
    extra = found_hosts - expected_hosts
    assert not missing, f"Missing statistics section(s) for: {', '.join(sorted(missing))}"
    assert not extra, f"Unexpected statistics section(s) for: {', '.join(sorted(extra))}"

    # Also verify that each stats line includes the key substrings the student
    # will need to parse.
    for ip, stats_line in stats_blocks:
        assert "packets transmitted" in stats_line and "received" in stats_line, (
            f"Stats line for {ip!r} does not include both 'packets transmitted' "
            f"and 'received':\n{stats_line}"
        )