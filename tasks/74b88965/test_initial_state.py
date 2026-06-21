# test_initial_state.py
"""
Pytest suite that verifies the initial state of the filesystem **before** the
student performs any actions for the “network-diagnostics summary” exercise.

The checks performed:

1. Required raw directory exists.
2. Required raw files exist and are regular files.
3. The yet-to-be-produced summary directory **does not** exist.
4. Contents of ping_localhost.txt contain the expected statistics.
5. Contents of ss_output.txt indicate exactly two TCP LISTEN sockets.
6. No summary artefacts (CSV / JSON) are present yet.

Any failure here means the grading environment is not in the expected pristine
state or the provided fixtures were modified.
"""

import os
import re
import json
import pytest
from pathlib import Path

HOME = Path("/home/user")
RAW_DIR = HOME / "network_diagnostics" / "raw"
SUMMARY_DIR = HOME / "network_diagnostics" / "2023-obs-summary"

PING_FILE = RAW_DIR / "ping_localhost.txt"
TRACEROUTE_FILE = RAW_DIR / "traceroute_localhost.txt"
SS_FILE = RAW_DIR / "ss_output.txt"

EXPECTED_PING_METRICS = {
    "packets_transmitted": 4,
    "packets_received": 4,
    "packet_loss_percent": 0,
    "rtt_min_ms": 0.025,
    "rtt_avg_ms": 0.029,
    "rtt_max_ms": 0.035,
}

EXPECTED_TCP_LISTEN = 2


# --------------------------------------------------------------------------- #
# Helper functions                                                            #
# --------------------------------------------------------------------------- #
def parse_ping_stats(text: str):
    """
    Parse the ping statistics section from a standard UNIX ping output.
    Returns a dict containing integer packet counts and float RTT figures.
    Raises ValueError if the expected patterns are not found.
    """
    # Example line:
    # 4 packets transmitted, 4 received, 0% packet loss, time 3058ms
    pkts_match = re.search(
        r"(?P<tx>\d+)\s+packets transmitted,\s+"
        r"(?P<rx>\d+)\s+received,\s+"
        r"(?P<loss>\d+)%\s+packet loss",
        text,
    )
    if not pkts_match:
        raise ValueError("Unable to locate packet statistics line in ping output.")

    # Example line:
    # rtt min/avg/max/mdev = 0.025/0.029/0.035/0.004 ms
    rtt_match = re.search(
        r"rtt min/avg/max/\w+\s*=\s*"
        r"(?P<min>[0-9.]+)/(?P<avg>[0-9.]+)/(?P<max>[0-9.]+)/",
        text,
    )
    if not rtt_match:
        raise ValueError("Unable to locate rtt statistics line in ping output.")

    stats = {
        "packets_transmitted": int(pkts_match.group("tx")),
        "packets_received": int(pkts_match.group("rx")),
        "packet_loss_percent": int(pkts_match.group("loss")),
        "rtt_min_ms": float(rtt_match.group("min")),
        "rtt_avg_ms": float(rtt_match.group("avg")),
        "rtt_max_ms": float(rtt_match.group("max")),
    }
    return stats


def count_tcp_listen_sockets(text: str) -> int:
    """
    Counts how many lines in the output of `ss` contain a TCP LISTEN socket.
    """
    count = 0
    for line in text.splitlines():
        # A simple split is sufficient for the synthetic fixture.
        parts = line.split()
        if len(parts) >= 2 and parts[0] == "tcp" and parts[1] == "LISTEN":
            count += 1
    return count


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #
def test_raw_directory_exists():
    assert RAW_DIR.is_dir(), f"Required directory missing: {RAW_DIR}"


@pytest.mark.parametrize(
    "file_path",
    [PING_FILE, TRACEROUTE_FILE, SS_FILE],
    ids=lambda p: str(p),
)
def test_each_raw_file_exists(file_path: Path):
    assert file_path.is_file(), f"Required file missing: {file_path}"


def test_summary_directory_absent():
    assert not SUMMARY_DIR.exists(), (
        f"Summary directory {SUMMARY_DIR} should NOT exist before the student "
        "creates it."
    )


def test_ping_file_contents_match_expected():
    text = PING_FILE.read_text()
    stats = parse_ping_stats(text)

    mismatches = {
        key: (stats[key], EXPECTED_PING_METRICS[key])
        for key in EXPECTED_PING_METRICS
        if stats[key] != EXPECTED_PING_METRICS[key]
    }
    assert not mismatches, (
        "ping_localhost.txt does not contain the expected statistics:\n"
        + json.dumps(mismatches, indent=2)
    )


def test_ss_output_contains_two_tcp_listen_sockets():
    text = SS_FILE.read_text()
    count = count_tcp_listen_sockets(text)
    assert (
        count == EXPECTED_TCP_LISTEN
    ), f"Expected {EXPECTED_TCP_LISTEN} TCP LISTEN sockets, found {count}."


def test_no_summary_files_exist_yet():
    csv_path = SUMMARY_DIR / "summary.csv"
    json_path = SUMMARY_DIR / "summary.json"
    assert not csv_path.exists(), (
        f"{csv_path} should NOT exist before the student runs their solution."
    )
    assert not json_path.exists(), (
        f"{json_path} should NOT exist before the student runs their solution."
    )