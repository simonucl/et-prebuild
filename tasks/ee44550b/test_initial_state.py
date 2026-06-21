# test_initial_state.py
#
# This pytest suite validates that the operating-system state **before** the
# student begins the task matches the specification in the assignment.
#
# It checks ONLY the pre-existing items (input directory / files) and does **not**
# touch or assert anything about the expected output path
# (/home/user/output or its contents).

import os
import pytest

SCAN_DIR = "/home/user/scan_results"
LOG_FILE = os.path.join(SCAN_DIR, "nmap_scan.log")

EXPECTED_LINES = [
    "192.168.1.10:22/tcp Open VULNERABLE-OpenSSH CVE-2020-1234",
    "192.168.1.12:80/tcp Closed",
    "192.168.1.15:445/tcp Open VULNERABLE-SMBGhost CVE-2020-0796",
    "10.0.0.5:3389/tcp Open Secure",
    "172.16.0.9:22/tcp Open VULNERABLE-OpenSSH CVE-2021-28041",
]


def test_scan_directory_exists():
    """The /home/user/scan_results directory must exist prior to the student's action."""
    assert os.path.isdir(
        SCAN_DIR
    ), f"Required directory '{SCAN_DIR}' is missing."


def test_log_file_exists():
    """The nmap scan log file must exist at the expected absolute path."""
    assert os.path.isfile(
        LOG_FILE
    ), f"Required log file '{LOG_FILE}' does not exist."


def test_log_file_contents_exact():
    """
    The log file must contain exactly the five expected lines, newline-terminated
    and in the correct order.
    """
    with open(LOG_FILE, "r", encoding="utf-8") as fh:
        # strip newline characters for comparison
        actual_lines = [line.rstrip("\n") for line in fh.readlines()]

    assert (
        actual_lines == EXPECTED_LINES
    ), (
        "The contents of the log file are not as expected.\n"
        "Expected:\n"
        + "\n".join(EXPECTED_LINES)
        + "\n\nActual:\n"
        + "\n".join(actual_lines)
    )