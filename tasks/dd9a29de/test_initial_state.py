# test_initial_state.py
#
# Pytest suite that verifies the operating-system / file-system state
# BEFORE the student’s solution runs.

import os
import stat
from pathlib import Path

RAW_DIR = Path("/home/user/raw_logs")
RAW_FILE = RAW_DIR / "ping_results.log"
OUTPUT_DIR = Path("/home/user/output")
SUMMARY_CSV = OUTPUT_DIR / "summary.csv"
ALERTS_LOG = OUTPUT_DIR / "alerts.log"


EXPECTED_PING_LOG = (
    "PING google.com (172.217.164.110) 56(84) bytes of data.\n"
    "64 bytes from 172.217.164.110: icmp_seq=1 ttl=115 time=14.3 ms\n"
    "64 bytes from 172.217.164.110: icmp_seq=2 ttl=115 time=15.8 ms\n"
    "64 bytes from 172.217.164.110: icmp_seq=3 ttl=115 time=16.1 ms\n"
    "64 bytes from 172.217.164.110: icmp_seq=4 ttl=115 time=15.7 ms\n"
    "\n"
    "--- 172.217.164.110 ping statistics ---\n"
    "4 packets transmitted, 4 received, 0% packet loss, time 3005ms\n"
    "rtt min/avg/max/mdev = 14.123/15.456/17.890/1.234 ms\n"
    "\n"
    "\n"
    "PING cloudflare.com (104.16.123.96) 56(84) bytes of data.\n"
    "64 bytes from 104.16.123.96: icmp_seq=1 ttl=59 time=22.4 ms\n"
    "64 bytes from 104.16.123.96: icmp_seq=2 ttl=59 time=23.1 ms\n"
    "64 bytes from 104.16.123.96: icmp_seq=3 ttl=59 time=22.8 ms\n"
    "64 bytes from 104.16.123.96: icmp_seq=4 ttl=59 time=22.5 ms\n"
    "\n"
    "--- 104.16.123.96 ping statistics ---\n"
    "4 packets transmitted, 4 received, 0% packet loss, time 4005ms\n"
    "rtt min/avg/max/mdev = 21.978/22.678/23.145/0.421 ms\n"
    "\n"
    "\n"
    "PING fileserver (10.0.0.5) 56(84) bytes of data.\n"
    "64 bytes from 10.0.0.5: icmp_seq=1 ttl=64 time=82.1 ms\n"
    "64 bytes from 10.0.0.5: icmp_seq=2 ttl=64 time=85.4 ms\n"
    "64 bytes from 10.0.0.5: icmp_seq=3 ttl=64 time=88.2 ms\n"
    "\n"
    "--- 10.0.0.5 ping statistics ---\n"
    "4 packets transmitted, 3 received, 25% packet loss, time 4007ms\n"
    "rtt min/avg/max/mdev = 80.567/85.234/89.105/3.456 ms\n"
    "\n"
    "\n"
    "PING remote_site (203.0.113.25) 56(84) bytes of data.\n"
    "64 bytes from 203.0.113.25: icmp_seq=2 ttl=46 time=109.9 ms\n"
    "64 bytes from 203.0.113.25: icmp_seq=4 ttl=46 time=110.8 ms\n"
    "\n"
    "--- 203.0.113.25 ping statistics ---\n"
    "4 packets transmitted, 2 received, 50% packet loss, time 3998ms\n"
    "rtt min/avg/max/mdev = 109.255/110.345/110.831/0.788 ms\n"
    "\n"
    "\n"
    "PING ipv6_google (2001:4860:4860::8888) 56(84) bytes of data.\n"
    "64 bytes from 2001:4860:4860::8888: icmp_seq=1 ttl=115 time=27.1 ms\n"
    "64 bytes from 2001:4860:4860::8888: icmp_seq=2 ttl=115 time=28.4 ms\n"
    "64 bytes from 2001:4860:4860::8888: icmp_seq=3 ttl=115 time=27.9 ms\n"
    "64 bytes from 2001:4860:4860::8888: icmp_seq=4 ttl=115 time=27.3 ms\n"
    "\n"
    "--- 2001:4860:4860::8888 ping statistics ---\n"
    "4 packets transmitted, 4 received, 0% packet loss, time 4006ms\n"
    "rtt min/avg/max/mdev = 26.987/27.890/28.431/0.517 ms\n"
)

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #


def _perm_bits(path: Path) -> int:
    """Return the permission bits (e.g., 0o755) of *path*."""
    return stat.S_IMODE(path.stat().st_mode)


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #


def test_raw_logs_directory_exists_and_has_correct_permissions():
    assert RAW_DIR.exists(), f"Required directory {RAW_DIR} is missing."
    assert RAW_DIR.is_dir(), f"{RAW_DIR} exists but is not a directory."
    expected_mode = 0o755
    actual_mode = _perm_bits(RAW_DIR)
    assert (
        actual_mode == expected_mode
    ), f"{RAW_DIR} permissions should be 755, found {oct(actual_mode)}."


def test_ping_results_log_exists_with_expected_content():
    assert RAW_FILE.exists(), f"Required file {RAW_FILE} is missing."
    assert RAW_FILE.is_file(), f"{RAW_FILE} exists but is not a regular file."

    with RAW_FILE.open("r", encoding="utf-8", newline="") as fh:
        contents = fh.read()

    # Allow for a single optional trailing newline at EOF by normalising
    if contents.endswith("\n") and not EXPECTED_PING_LOG.endswith("\n"):
        contents = contents[:-1]

    assert (
        contents == EXPECTED_PING_LOG
    ), (
        f"Contents of {RAW_FILE} do not match the expected initial ping log.\n"
        "If you edited this file, restore it exactly as provided in the task "
        "description (including blank lines)."
    )


def test_output_directory_absent_before_student_runs():
    assert (
        not OUTPUT_DIR.exists()
    ), f"{OUTPUT_DIR} should NOT exist before the student's solution runs."


def test_no_output_files_present_yet():
    assert (
        not SUMMARY_CSV.exists()
    ), f"File {SUMMARY_CSV} should not exist in the initial state."
    assert (
        not ALERTS_LOG.exists()
    ), f"File {ALERTS_LOG} should not exist in the initial state."