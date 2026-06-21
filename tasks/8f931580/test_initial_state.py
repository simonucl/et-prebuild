# test_initial_state.py
"""
Pytest suite that validates the environment *before* the student performs any
actions for the “critical remote-access services” task.

Expectations for the pristine container:
1. /home/user/scans/full_scan.log exists and its contents are **exactly** the
   provided Nmap scan output.
2. /home/user/reports directory does **NOT** exist yet.
3. /home/user/reports/critical_ports.csv does **NOT** exist yet.

If any of these checks fail, the learner is starting from the wrong baseline
and the assessment will be unreliable.
"""

import os
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# Constants                                                                   
# --------------------------------------------------------------------------- #

SCAN_FILE = Path("/home/user/scans/full_scan.log")
REPORTS_DIR = Path("/home/user/reports")
REPORT_FILE = REPORTS_DIR / "critical_ports.csv"

# The exact contents that must already be on disk.
# A trailing newline after the final line *is* part of the expected content.
EXPECTED_SCAN_CONTENT = (
    "Starting Nmap 7.80 ( https://nmap.org ) at 2023-11-18 14:12 UTC\n"
    "Nmap scan report for target1.local (192.168.0.5)\n"
    "Host is up (0.00032s latency).\n"
    "Not shown: 997 closed ports\n"
    "PORT     STATE SERVICE     VERSION\n"
    "22/tcp   open  ssh         OpenSSH 8.2p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)\n"
    "80/tcp   open  http        Apache httpd 2.4.41 ((Ubuntu))\n"
    "443/tcp  open  ssl/http    Apache httpd 2.4.41 ((Ubuntu))\n"
    "| ssl-cert: Subject: commonName=target1.local\n"
    "|_Not valid before: 2020-01-15T12:49:00\n"
    "Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel\n"
    "\n"
    "Nmap scan report for 192.168.0.10\n"
    "Host is up (0.0011s latency).\n"
    "Not shown: 996 closed ports\n"
    "PORT     STATE SERVICE VERSION\n"
    "21/tcp   open  ftp     vsftpd 3.0.3\n"
    "| ftp-anon: Anonymous FTP login allowed (FTP code 230)\n"
    "| -\n"
    "|_-rw-r--r--   1 ftp      ftp          1234 Jan 01 2020 readme.txt\n"
    "23/tcp   open  telnet  Linux telnetd\n"
    "445/tcp  open  smb      Samba smbd 4.11.6 (workgroup: WORKGROUP)\n"
    "Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel\n"
    "\n"
    "Nmap done: 2 IP addresses (2 hosts up) scanned in 8.71 seconds\n"
)

# --------------------------------------------------------------------------- #
# Tests                                                                       
# --------------------------------------------------------------------------- #


def test_scan_file_exists():
    """The Nmap scan log must be present before the student starts."""
    assert SCAN_FILE.exists(), (
        f"Required scan file {SCAN_FILE} is missing.\n"
        "Without this file, the learner cannot complete the exercise."
    )
    assert SCAN_FILE.is_file(), f"{SCAN_FILE} exists but is not a regular file."


def test_scan_file_content_exact_match():
    """
    The scan file must contain the exact, unaltered Nmap output provided
    in the task description.
    """
    actual_content = SCAN_FILE.read_text(encoding="utf-8")
    assert actual_content == EXPECTED_SCAN_CONTENT, (
        "The contents of the scan file do not match the expected baseline.\n"
        "If this file has been modified, the learner will extract incorrect "
        "data. Revert it to the original, byte-for-byte content."
    )


def test_reports_directory_absent():
    """
    The reports directory must NOT exist yet; the learner is expected to
    create it as part of the task.
    """
    assert not REPORTS_DIR.exists(), (
        f"Directory {REPORTS_DIR} already exists but should not. "
        "Remove it so the learner can practice creating it."
    )


def test_critical_csv_absent():
    """
    The final CSV report must NOT exist at the start of the exercise.
    """
    assert not REPORT_FILE.exists(), (
        f"File {REPORT_FILE} already exists but should not. "
        "Delete it so the learner can generate a fresh report."
    )