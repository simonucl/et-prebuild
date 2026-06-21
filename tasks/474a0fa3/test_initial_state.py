# test_initial_state.py
#
# This test-suite validates the **initial** operating-system / filesystem
# state *before* the student’s solution is run.  If these tests fail, the
# grading rig itself is not in the expected starting condition.

import os
import stat
from pathlib import Path

import pytest

PROJECT_ROOT = Path("/home/user/project")
LOGS_DIR = PROJECT_ROOT / "logs"
ACCESS_LOG = LOGS_DIR / "access.log"
REPORTS_DIR = PROJECT_ROOT / "reports"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _perm_bits(path: Path) -> int:
    """
    Return the permission bits (the lowest 9 bits) for the given path.
    Same as the octal part you would see in ``ls -l``.
    """
    return stat.S_IMODE(path.stat().st_mode)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_access_log_exists_and_is_regular_file():
    assert ACCESS_LOG.exists(), (
        f"Missing required log file: {ACCESS_LOG}. "
        "The initial fixture must contain this file."
    )
    assert ACCESS_LOG.is_file(), f"{ACCESS_LOG} exists but is not a regular file."
    # Readability: user/owner should be able to read. 644 ≤ mode
    perms = _perm_bits(ACCESS_LOG)
    assert perms & stat.S_IRUSR, f"{ACCESS_LOG} is not readable (perm bits {oct(perms)})."


def test_access_log_contents_exact_match():
    expected_content = (
        "127.0.0.1 - - [10/Jul/2023:22:55:36 +0000] \"GET /index.html HTTP/1.1\" 200 1043 \"-\" \"Mozilla/5.0\"\n"
        "192.168.1.10 - - [10/Jul/2023:22:56:01 +0000] \"GET /nonexistent.html HTTP/1.1\" 404 512 \"-\" \"Mozilla/5.0\"\n"
        "172.16.0.2 - - [10/Jul/2023:22:56:05 +0000] \"GET /missing.png HTTP/1.1\" 404 512 \"-\" \"Mozilla/5.0\"\n"
        "10.0.0.5 - - [10/Jul/2023:22:56:10 +0000] \"POST /api/v1/users HTTP/1.1\" 500 2560 \"-\" \"curl/7.68.0\"\n"
        "192.168.1.10 - - [10/Jul/2023:22:56:21 +0000] \"GET /typo.html HTTP/1.1\" 404 512 \"-\" \"Mozilla/5.0\"\n"
        "10.0.0.5 - - [10/Jul/2023:22:56:23 +0000] \"GET /server-error HTTP/1.1\" 500 2048 \"-\" \"Mozilla/5.0\"\n"
        "172.16.0.2 - - [10/Jul/2023:22:56:30 +0000] \"GET /another-missing.html HTTP/1.1\" 404 512 \"-\" \"Mozilla/5.0\"\n"
        "203.0.113.9 - - [10/Jul/2023:22:56:40 +0000] \"GET /redirect HTTP/1.1\" 301 234 \"-\" \"Mozilla/5.0\"\n"
        "192.168.1.10 - - [10/Jul/2023:22:57:01 +0000] \"GET /old-page HTTP/1.1\" 301 234 \"-\" \"Mozilla/5.0\"\n"
        "10.0.0.5 - - [10/Jul/2023:22:57:10 +0000] \"GET /server-error HTTP/1.1\" 500 2048 \"-\" \"Mozilla/5.0\"\n"
        "192.168.1.10 - - [10/Jul/2023:22:57:21 +0000] \"GET /contact.html HTTP/1.1\" 200 1345 \"-\" \"Mozilla/5.0\"\n"
        "10.0.0.5 - - [10/Jul/2023:22:57:44 +0000] \"POST /api/v1/users HTTP/1.1\" 500 2560 \"-\" \"curl/7.68.0\"\n"
        "192.0.2.44 - - [10/Jul/2023:22:58:00 +0000] \"GET /server-error HTTP/1.1\" 500 2048 \"-\" \"Mozilla/5.0\"\n"
        "10.0.0.5 - - [10/Jul/2023:22:58:10 +0000] \"GET /server-error HTTP/1.1\" 500 2048 \"-\" \"Mozilla/5.0\"\n"
        "172.16.0.2 - - [10/Jul/2023:22:58:11 +0000] \"GET /redirect HTTP/1.1\" 301 234 \"-\" \"Mozilla/5.0\"\n"
        "203.0.113.9 - - [10/Jul/2023:22:58:20 +0000] \"GET /login HTTP/1.1\" 500 1234 \"-\" \"Mozilla/5.0\"\n"
        "203.0.113.9 - - [10/Jul/2023:22:58:25 +0000] \"GET /login HTTP/1.1\" 500 1234 \"-\" \"Mozilla/5.0\"\n"
        "203.0.113.9 - - [10/Jul/2023:22:58:30 +0000] \"GET /purchase HTTP/1.1\" 500 1456 \"-\" \"Mozilla/5.0\"\n"
        "198.51.100.13 - - [10/Jul/2023:22:58:40 +0000] \"GET /admin HTTP/1.1\" 500 1820 \"-\" \"Mozilla/5.0\"\n"
        "203.0.113.9 - - [10/Jul/2023:22:58:50 +0000] \"GET /api/v1/users HTTP/1.1\" 500 2560 \"-\" \"curl/7.68.0\"\n"
        "203.0.113.25 - - [10/Jul/2023:22:59:01 +0000] \"GET /api/v1/users HTTP/1.1\" 500 2560 \"-\" \"curl/7.68.0\"\n"
        "203.0.113.9 - - [10/Jul/2023:22:59:10 +0000] \"GET /server-error HTTP/1.1\" 500 2048 \"-\" \"Mozilla/5.0\"\n"
        "192.168.1.10 - - [10/Jul/2023:22:59:30 +0000] \"GET /still-missing.html HTTP/1.1\" 404 512 \"-\" \"Mozilla/5.0\"\n"
        "10.0.0.5 - - [10/Jul/2023:22:59:45 +0000] \"GET /lost.html HTTP/1.1\" 404 512 \"-\" \"Mozilla/5.0\"\n"
    )
    with ACCESS_LOG.open("r", encoding="utf-8") as fh:
        actual = fh.read()
    assert (
        actual == expected_content
    ), "Contents of access.log do not match the expected fixture."


def test_no_reports_directory_yet():
    assert not REPORTS_DIR.exists(), (
        f"{REPORTS_DIR} should NOT exist at the start of the exercise. "
        "The student is responsible for creating it."
    )


def test_logs_directory_contains_only_access_log():
    assert LOGS_DIR.exists() and LOGS_DIR.is_dir(), f"Missing directory {LOGS_DIR}"
    entries = [p.name for p in LOGS_DIR.iterdir() if not p.name.startswith(".")]
    assert entries == ["access.log"], (
        f"{LOGS_DIR} should contain only 'access.log' initially, "
        f"but found: {entries}"
    )