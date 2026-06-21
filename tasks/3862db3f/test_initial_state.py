# test_initial_state.py
#
# Pytest suite that validates the OS / filesystem _before_ the student
# performs any action for the “quick vulnerability triage” exercise.

import os
import stat
import pytest
from pathlib import Path


HOME = Path("/home/user")
INPUT_DIR = HOME / "vuln_scan" / "input"
BANNERS_FILE = INPUT_DIR / "banners.txt"
REPORT_DIR = HOME / "vuln_scan" / "report"
REPORT_FILE = REPORT_DIR / "vulnerability_report.log"


EXPECTED_BANNERS_CONTENT = (
    "80/tcp open  http  Apache httpd 2.2.15 (CentOS)\n"
    "22/tcp open  ssh   OpenSSH 6.0p1 Debian 4+deb7u2 (protocol 2.0)\n"
    "443/tcp open  ssl/openssl  OpenSSL 1.0.1e\n"
    "21/tcp open  ftp   vsftpd 2.3.4\n"
).encode()  # compare in binary to avoid encoding surprises


def test_input_directory_exists():
    """
    The directory /home/user/vuln_scan/input/ must exist **before** the task starts.
    """
    assert INPUT_DIR.exists(), (
        f"Required directory {INPUT_DIR} is missing. "
        "It must be present before the student begins."
    )
    assert INPUT_DIR.is_dir(), (
        f"{INPUT_DIR} exists but is not a directory."
    )
    # Directory should be at least readable and executable by the current user
    st_mode = INPUT_DIR.stat().st_mode
    assert st_mode & stat.S_IRUSR and st_mode & stat.S_IXUSR, (
        f"{INPUT_DIR} must be readable and searchable by the current user."
    )


def test_banners_file_exists_and_is_correct():
    """
    The banners.txt file must exist with the exact expected byte content.
    """
    assert BANNERS_FILE.exists(), (
        f"Required file {BANNERS_FILE} is missing."
    )
    assert BANNERS_FILE.is_file(), (
        f"{BANNERS_FILE} exists but is not a regular file."
    )
    st_mode = BANNERS_FILE.stat().st_mode
    assert st_mode & stat.S_IRUSR, (
        f"{BANNERS_FILE} is not readable by the current user."
    )

    with BANNERS_FILE.open("rb") as fp:
        actual = fp.read()

    assert actual == EXPECTED_BANNERS_CONTENT, (
        f"{BANNERS_FILE} contents do not match the expected data.\n"
        "If you modified this file or its newline termination, revert the change.\n"
        "Expected (bytes):\n"
        f"{EXPECTED_BANNERS_CONTENT!r}\n\nGot (bytes):\n{actual!r}"
    )


def test_report_file_not_present_yet():
    """
    Before the student runs their solution, the vulnerability report **must not** exist.
    The exercise requires the student to create it.
    """
    assert not REPORT_FILE.exists(), (
        f"The report file {REPORT_FILE} already exists, but the exercise "
        "requires the student to create it."
    )