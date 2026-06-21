# test_initial_state.py
#
# This test-suite verifies that the *initial* operating-system / filesystem
# state is exactly what the assignment presumes **before** the student starts
# working.  It intentionally does NOT look for any artefacts that the student
# is supposed to create later (e.g. /home/user/output or its files).

import os
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# Constants describing the required initial state
# --------------------------------------------------------------------------- #

SERVER_LOG_DIR = Path("/home/user/server_logs")
ACCESS_LOG_FILE = SERVER_LOG_DIR / "access.log"

# The exact 31 log-lines that must already be present in access.log,
# each terminated by a single Unix LF (`\n`).
EXPECTED_ACCESS_LOG_LINES = [
    '192.168.0.1 - - [12/Jun/2023:10:00:01 +0000] "GET /index.html HTTP/1.1" 200 1024\n',
    '192.168.0.1 - - [12/Jun/2023:10:01:35 +0000] "POST /login HTTP/1.1" 302 512\n',
    '10.0.0.5 - - [12/Jun/2023:10:02:10 +0000] "GET /about.html HTTP/1.1" 200 2048\n',
    '203.0.113.10 - - [12/Jun/2023:10:03:22 +0000] "GET /contact.html HTTP/1.1" 404 256\n',
    '192.168.0.1 - - [12/Jun/2023:10:04:05 +0000] "GET /products.html HTTP/1.1" 200 4096\n',
    '198.51.100.22 - - [12/Jun/2023:10:05:47 +0000] "GET /index.html HTTP/1.1" 500 1024\n',
    '172.16.0.7 - - [12/Jun/2023:10:06:58 +0000] "GET /index.html HTTP/1.1" 200 1024\n',
    '192.0.2.44 - - [12/Jun/2023:10:07:11 +0000] "GET /downloads/file.zip HTTP/1.1" 200 8192\n',
    '10.0.0.5 - - [12/Jun/2023:10:08:14 +0000] "GET /index.html HTTP/1.1" 200 1024\n',
    '203.0.113.10 - - [12/Jun/2023:10:09:33 +0000] "GET /blog HTTP/1.1" 200 512\n',
    '198.18.0.1 - - [12/Jun/2023:10:10:02 +0000] "GET /index.html HTTP/1.1" 404 256\n',
    '127.0.0.1 - - [12/Jun/2023:10:10:30 +0000] "GET /server-status HTTP/1.1" 200 1024\n',
    '192.168.0.1 - - [12/Jun/2023:10:11:44 +0000] "GET /pricing.html HTTP/1.1" 404 256\n',
    '172.16.0.7 - - [12/Jun/2023:10:12:15 +0000] "POST /api/data HTTP/1.1" 500 128\n',
    '192.0.2.44 - - [12/Jun/2023:10:13:59 +0000] "GET /downloads/file2.zip HTTP/1.1" 200 4096\n',
    '192.168.0.1 - - [12/Jun/2023:10:14:26 +0000] "GET /index.html HTTP/1.1" 200 1024\n',
    '203.0.113.10 - - [12/Jun/2023:10:15:55 +0000] "GET /contact.html HTTP/1.1" 404 256\n',
    '10.0.0.5 - - [12/Jun/2023:10:16:37 +0000] "GET /search?q=test HTTP/1.1" 200 512\n',
    '198.51.100.22 - - [12/Jun/2023:10:17:48 +0000] "GET /index.html HTTP/1.1" 500 1024\n',
    '198.18.0.1 - - [12/Jun/2023:10:18:25 +0000] "GET /docs/manual.pdf HTTP/1.1" 200 2048\n',
    '172.16.0.7 - - [12/Jun/2023:10:19:11 +0000] "GET /support HTTP/1.1" 200 1024\n',
    '192.168.0.1 - - [12/Jun/2023:10:20:48 +0000] "POST /login HTTP/1.1" 302 512\n',
    '127.0.0.1 - - [12/Jun/2023:10:21:30 +0000] "GET /server-status HTTP/1.1" 200 1024\n',
    '10.0.0.5 - - [12/Jun/2023:10:22:07 +0000] "GET /index.html HTTP/1.1" 404 256\n',
    '203.0.113.10 - - [12/Jun/2023:10:23:59 +0000] "GET /blog HTTP/1.1" 200 512\n',
    '192.168.0.1 - - [12/Jun/2023:10:24:26 +0000] "GET /index.html HTTP/1.1" 200 1024\n',
    '198.51.100.22 - - [12/Jun/2023:10:25:48 +0000] "GET /health HTTP/1.1" 200 128\n',
    '192.168.0.1 - - [12/Jun/2023:10:26:15 +0000] "GET /dashboard HTTP/1.1" 200 1024\n',
    '10.0.0.5 - - [12/Jun/2023:10:27:37 +0000] "GET /search?q=linux HTTP/1.1" 500 256\n',
    '203.0.113.11 - - [12/Jun/2023:10:28:48 +0000] "GET /index.html HTTP/1.1" 200 1024\n',
    '192.0.2.45 - - [12/Jun/2023:10:29:29 +0000] "GET /robots.txt HTTP/1.1" 404 128\n',
]


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #

def test_server_log_directory_exists():
    """The directory /home/user/server_logs must already exist."""
    assert SERVER_LOG_DIR.is_dir(), (
        f"Expected directory {SERVER_LOG_DIR!s} to exist, "
        "but it is missing."
    )


def test_access_log_file_exists():
    """access.log must be present and be a regular readable file."""
    assert ACCESS_LOG_FILE.is_file(), (
        f"Expected file {ACCESS_LOG_FILE!s} to exist, "
        "but it is missing."
    )
    assert os.access(ACCESS_LOG_FILE, os.R_OK), (
        f"File {ACCESS_LOG_FILE!s} exists but is not readable."
    )


def test_access_log_file_contents_are_exact():
    """
    access.log must contain *exactly* the 31 lines provided in the exercise,
    each terminated by Unix LF.  Any deviation means the starting state is
    wrong and the student cannot reasonably succeed.
    """
    with ACCESS_LOG_FILE.open("r", encoding="utf-8", newline="") as fh:
        actual_lines = fh.readlines()

    # Basic sanity check: correct number of lines
    assert len(actual_lines) == len(EXPECTED_ACCESS_LOG_LINES), (
        f"{ACCESS_LOG_FILE!s} contains {len(actual_lines)} lines, "
        f"but {len(EXPECTED_ACCESS_LOG_LINES)} were expected."
    )

    # Compare line-by-line for full fidelity
    for idx, (expected, actual) in enumerate(
        zip(EXPECTED_ACCESS_LOG_LINES, actual_lines), start=1
    ):
        assert actual == expected, (
            f"Mismatch on line {idx} of {ACCESS_LOG_FILE!s}.\n"
            f"Expected: {expected!r}\n"
            f"Actual  : {actual!r}"
        )