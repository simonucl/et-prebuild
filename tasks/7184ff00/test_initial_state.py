# test_initial_state.py
#
# This pytest suite validates that the starting filesystem state for the
# “critical-vulnerability extraction” exercise is correct *before* the student
# begins working.  It checks only the pre-existing inputs and **intentionally
# ignores** any output paths that the student will create later.
#
# Expectations verified here:
#   1. /home/user/scans exists and is a directory.
#   2. /home/user/scans/nmap_scan.log exists, is a regular file, is readable,
#      has mode 0o644, and contains exactly the 12 expected lines (with a final
#      trailing newline).
#
# Any mismatch will raise a clear assertion error explaining what is wrong.

import os
import stat
from pathlib import Path

import pytest


SCAN_DIR = Path("/home/user/scans")
SCAN_FILE = SCAN_DIR / "nmap_scan.log"

# Exact expected file content (12 lines, each terminated by \n)
EXPECTED_LINES = [
    "192.168.1.10:22/tcp open ssh (protocol 2.0) | vuln: openssh-cve-2018-15473",
    "192.168.1.12:80/tcp open http apache 2.4.29 | vuln: cve-2021-41773",
    "192.168.1.15:443/tcp open https nginx 1.14.0",
    "192.168.1.20:23/tcp closed telnet",
    "192.168.1.30:3306/tcp open mysql 5.7.31 | vuln: cve-2019-5480",
    "192.168.1.35:25/tcp open smtp postfix",
    "192.168.1.40:8080/tcp open http-proxy squid 3.5 | vuln: cve-2019-12529",
    "10.0.0.5:53/udp open domain bind 9.10.3-P4",
    "10.0.0.8:110/tcp open pop3 dovecot 2.3.13 | vuln: cve-2020-10967",
    "10.0.0.9:995/tcp open pop3s dovecot 2.3.13",
    "10.0.0.10:143/tcp open imap dovecot 2.3.13 | vuln: cve-2020-25275",
    "10.0.0.20:21/tcp open ftp vsftpd 3.0.3 | vuln: cve-2011-2523",
]
EXPECTED_CONTENT = ("\n".join(EXPECTED_LINES) + "\n").encode()


def test_scan_directory_exists_and_is_directory():
    assert SCAN_DIR.exists(), f"Required directory not found: {SCAN_DIR}"
    assert SCAN_DIR.is_dir(), f"{SCAN_DIR} exists but is not a directory"


def test_scan_file_exists_and_is_regular_file():
    assert SCAN_FILE.exists(), f"Required file not found: {SCAN_FILE}"
    assert SCAN_FILE.is_file(), f"{SCAN_FILE} exists but is not a regular file"


def test_scan_file_permissions():
    mode = SCAN_FILE.stat().st_mode
    # Mask to permission bits only
    perm_bits = stat.S_IMODE(mode)
    expected_perm = 0o644
    assert (
        perm_bits == expected_perm
    ), f"{SCAN_FILE} permissions are {oct(perm_bits)}, expected {oct(expected_perm)}"


def test_scan_file_content_exact_match():
    content = SCAN_FILE.read_bytes()
    assert (
        content == EXPECTED_CONTENT
    ), (
        f"{SCAN_FILE} content does not match the expected 12-line fixture.\n"
        f"Hint: ensure no extra/missing lines or whitespace."
    )


def test_scan_file_line_count():
    with SCAN_FILE.open("r", encoding="utf-8") as fh:
        lines = fh.readlines()
    assert len(lines) == 12, f"{SCAN_FILE} should contain 12 lines, found {len(lines)}"
    # Additional sanity: every line (except possibly the last) MUST end with '\n'.
    for idx, line in enumerate(lines, start=1):
        assert line.endswith(
            "\n"
        ), f"Line {idx} of {SCAN_FILE} is missing a terminating newline character"