# test_initial_state.py
#
# This pytest suite validates the initial state of the filesystem **before**
# the student starts working on the task.  It checks that the raw Apache
# access log exists at the expected location and that its contents are
# exactly what the exercise description promises.
#
# NOTE: Per the grading rules we explicitly avoid looking at (or for) any
#       output files or directories – we only assert the presence and
#       correctness of the input log file.

import pathlib
import pytest

PROJECT_ROOT = pathlib.Path("/home/user/project")
ACCESS_LOG = PROJECT_ROOT / "access.log"

# Expected 20-line log as specified in the task description.
EXPECTED_LINES = [
    '127.0.0.1 - - [10/Jan/2023:13:55:36 +0000] "GET /index.html HTTP/1.1" 200 1024',
    '192.168.0.2 - - [10/Jan/2023:13:56:01 +0000] "POST /login HTTP/1.1" 302 512',
    '10.0.0.5 - - [10/Jan/2023:13:56:18 +0000] "GET /dashboard HTTP/1.1" 200 2048',
    '127.0.0.1 - - [10/Jan/2023:13:57:42 +0000] "GET /favicon.ico HTTP/1.1" 404 209',
    '192.168.0.2 - - [10/Jan/2023:13:58:12 +0000] "GET /profile HTTP/1.1" 200 2304',
    '10.0.0.5 - - [10/Jan/2023:13:59:03 +0000] "GET /settings HTTP/1.1" 200 1900',
    '203.0.113.9 - - [10/Jan/2023:14:00:11 +0000] "GET /index.html HTTP/1.1" 200 1024',
    '198.51.100.4 - - [10/Jan/2023:14:01:20 +0000] "GET /doesnotexist HTTP/1.1" 404 512',
    '192.168.0.2 - - [10/Jan/2023:14:02:27 +0000] "POST /login HTTP/1.1" 302 512',
    '203.0.113.9 - - [10/Jan/2023:14:03:31 +0000] "GET /index.html HTTP/1.1" 200 1024',
    '10.0.0.5 - - [10/Jan/2023:14:04:02 +0000] "GET /dashboard HTTP/1.1" 200 2048',
    '198.51.100.4 - - [10/Jan/2023:14:05:45 +0000] "GET /favicon.ico HTTP/1.1" 404 209',
    '127.0.0.1 - - [10/Jan/2023:14:06:30 +0000] "GET /index.html HTTP/1.1" 200 1024',
    '192.168.0.2 - - [10/Jan/2023:14:07:12 +0000] "GET /profile HTTP/1.1" 200 2304',
    '203.0.113.9 - - [10/Jan/2023:14:07:59 +0000] "GET /settings HTTP/1.1" 200 1900',
    '127.0.0.1 - - [10/Jan/2023:14:08:46 +0000] "POST /login HTTP/1.1" 302 512',
    '203.0.113.9 - - [10/Jan/2023:14:09:37 +0000] "GET /doesnotexist HTTP/1.1" 404 512',
    '198.51.100.4 - - [10/Jan/2023:14:10:15 +0000] "GET /index.html HTTP/1.1" 200 1024',
    '10.0.0.5 - - [10/Jan/2023:14:10:54 +0000] "GET /profile HTTP/1.1" 200 2304',
    '192.168.0.2 - - [10/Jan/2023:14:11:33 +0000] "GET /favicon.ico HTTP/1.1" 404 209',
]


def _read_log_lines():
    """Utility helper that returns the access.log content split into lines."""
    return ACCESS_LOG.read_text(encoding="utf-8").splitlines()


def test_access_log_exists_and_is_a_file():
    assert ACCESS_LOG.exists(), f"Expected log file {ACCESS_LOG} to exist."
    assert ACCESS_LOG.is_file(), f"Expected {ACCESS_LOG} to be a regular file."


def test_access_log_has_expected_number_of_lines():
    lines = _read_log_lines()
    expected_count = 20
    assert len(lines) == expected_count, (
        f"{ACCESS_LOG} should contain {expected_count} lines, "
        f"but actually contains {len(lines)}."
    )


def test_access_log_contents_match_exactly():
    lines = _read_log_lines()
    assert lines == EXPECTED_LINES, (
        f"The contents of {ACCESS_LOG} do not match the expected starter data.\n"
        "If you modified the log, please restore it exactly as provided."
    )


def test_access_log_ends_with_newline():
    data = ACCESS_LOG.read_bytes()
    assert data.endswith(b"\n"), (
        f"{ACCESS_LOG} must end with a newline character."
    )