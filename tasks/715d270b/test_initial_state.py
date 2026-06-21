# test_initial_state.py
"""
Pytest suite that validates the initial operating-system / filesystem state
BEFORE the student runs any commands for the “404 Not Found” log-analysis task.

This file checks ONLY the pre-existing resources.  It deliberately avoids
touching, mentioning, or asserting anything about the *output* artefacts
(e.g. /home/user/webapp/reports or 404_ips.txt) so as not to violate
the grading constraints.
"""

import os
import stat
from pathlib import Path

ACCESS_LOG = Path("/home/user/webapp/logs/access.log")

# Expected contents of the pre-existing Apache-style access log.
EXPECTED_LOG_CONTENT = (
    '127.0.0.1 - - [12/Jun/2023:10:55:32 +0000] "GET /index.html HTTP/1.1" 200 1024 "-" "Mozilla/5.0"\n'
    '192.168.0.42 - - [12/Jun/2023:10:55:35 +0000] "GET /does-not-exist HTTP/1.1" 404 512 "-" "Mozilla/5.0"\n'
    '10.10.10.10 - - [12/Jun/2023:10:55:37 +0000] "POST /login HTTP/1.1" 302 256 "-" "Mozilla/5.0"\n'
    '172.16.0.5 - - [12/Jun/2023:10:55:40 +0000] "GET /admin HTTP/1.1" 403 2048 "-" "Mozilla/5.0"\n'
    '192.168.0.42 - - [12/Jun/2023:10:55:45 +0000] "GET /another-missing HTTP/1.1" 404 512 "-" "Mozilla/5.0"\n'
    '203.0.113.77 - - [12/Jun/2023:10:55:50 +0000] "GET /favicon.ico HTTP/1.1" 404 128 "-" "Mozilla/5.0"\n'
    '127.0.0.1 - - [12/Jun/2023:10:56:01 +0000] "GET /assets/css/main.css HTTP/1.1" 200 4096 "-" "Mozilla/5.0"\n'
)


def test_webapp_directories_exist():
    """Verify that /home/user/webapp and /home/user/webapp/logs exist."""
    webapp_dir = Path("/home/user/webapp")
    logs_dir = webapp_dir / "logs"

    assert webapp_dir.is_dir(), (
        f"Expected directory {webapp_dir} to exist, but it is missing."
    )
    assert logs_dir.is_dir(), (
        f"Expected directory {logs_dir} to exist, but it is missing."
    )


def test_access_log_file_exists():
    """Ensure the access.log file exists and is a regular file."""
    assert ACCESS_LOG.exists(), (
        f"Expected log file {ACCESS_LOG} to exist, but it is missing."
    )
    assert ACCESS_LOG.is_file(), (
        f"{ACCESS_LOG} exists, but it is not a regular file."
    )


def test_access_log_permissions():
    """
    access.log must have permissions 0644.
    Only permission bits are compared—ownership is not enforced here.
    """
    st_mode = ACCESS_LOG.stat().st_mode
    perms = stat.S_IMODE(st_mode)
    expected_perms = 0o644
    assert perms == expected_perms, (
        f"{ACCESS_LOG} has permissions {oct(perms)}, but expected {oct(expected_perms)}."
    )


def test_access_log_contents_exact_match():
    """The contents of access.log must match the canonical initial dataset."""
    actual = ACCESS_LOG.read_text(encoding="utf-8")
    assert actual == EXPECTED_LOG_CONTENT, (
        "The contents of the initial access.log do not match the expected "
        "fixture.  Make sure the file has not been modified."
    )