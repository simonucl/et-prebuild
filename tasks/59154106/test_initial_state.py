# test_initial_state.py
#
# This pytest file validates the **initial** operating-system state
# before the student runs any commands.  It deliberately avoids
# checking for *output* artefacts that the student will create later.
#
# What is verified:
#   1. /home/user/logs/ exists and is a directory.
#   2. /home/user/logs/webserver_access.log exists, is a regular file, and
#      contains exactly the 15 expected log lines in the right order
#      (including a single trailing newline).
#
# Only stdlib + pytest are used.

import os
from pathlib import Path
import stat
import pytest

LOG_DIR = Path("/home/user/logs")
ACCESS_LOG = LOG_DIR / "webserver_access.log"

# The exact 15 lines that must be present in the access log *before* the student
# performs any action.  Each string purposefully excludes the trailing "\n".
EXPECTED_LOG_LINES = [
    '203.0.113.1 - - [15/Feb/2023:08:57:03 +0000] "GET /index.html HTTP/1.1" 200 1024',
    '198.51.100.2 - - [15/Feb/2023:09:10:44 +0000] "GET /about HTTP/1.1" 200 850',
    '192.0.2.3 - - [14/Feb/2023:23:59:59 +0000] "GET / HTTP/1.1" 200 600',
    '203.0.113.1 - - [15/Feb/2023:09:12:15 +0000] "POST /login HTTP/1.1" 302 517',
    '198.51.100.2 - - [15/Feb/2023:09:13:47 +0000] "GET /dashboard HTTP/1.1" 200 2048',
    '203.0.113.1 - - [15/Feb/2023:09:14:23 +0000] "GET /index.html HTTP/1.1" 200 1024',
    '203.0.113.1 - - [15/Feb/2023:09:20:55 +0000] "GET /products HTTP/1.1" 200 4096',
    '192.0.2.3 - - [15/Feb/2023:09:22:07 +0000] "GET /contact HTTP/1.1" 404 256',
    '198.51.100.2 - - [15/Feb/2023:09:30:18 +0000] "GET /pricing HTTP/1.1" 200 1536',
    '203.0.113.5 - - [16/Feb/2023:07:00:01 +0000] "GET /old-page HTTP/1.1" 301 245',
    '203.0.113.1 - - [15/Feb/2023:10:01:33 +0000] "GET /blog HTTP/1.1" 200 11200',
    '198.51.100.9 - - [15/Feb/2023:11:22:10 +0000] "GET /random HTTP/1.1" 200 100',
    '203.0.113.7 - - [13/Feb/2023:17:45:22 +0000] "GET /archive HTTP/1.1" 200 640',
    '192.0.2.3 - - [15/Feb/2023:12:00:00 +0000] "GET /contact HTTP/1.1" 404 256',
    '203.0.113.1 - - [15/Feb/2023:12:15:45 +0000] "GET /cart HTTP/1.1" 200 768',
]


def _is_regular_file(path: Path) -> bool:
    """Return True iff *path* exists and is a regular file."""
    try:
        mode = path.stat().st_mode
    except FileNotFoundError:
        return False
    return stat.S_ISREG(mode)


def test_logs_directory_exists():
    assert LOG_DIR.exists(), f"Required directory {LOG_DIR} is missing."
    assert LOG_DIR.is_dir(), f"{LOG_DIR} exists but is not a directory."


def test_access_log_file_exists_and_is_regular():
    assert _is_regular_file(ACCESS_LOG), (
        f"Expected regular file {ACCESS_LOG} is missing or not a regular file."
    )


def test_access_log_has_expected_content():
    # Read the entire file exactly as-is.
    data = ACCESS_LOG.read_text(encoding="utf-8")
    assert data.endswith(
        "\n"
    ), f"{ACCESS_LOG} must end with a single trailing newline."
    lines = data.splitlines()  # removes the trailing '\n'

    # Ensure line count is correct.
    assert (
        len(lines) == 15
    ), f"{ACCESS_LOG} should contain exactly 15 lines, found {len(lines)}."

    # Verify every line matches the expected content in the correct order.
    for idx, (got, expected) in enumerate(zip(lines, EXPECTED_LOG_LINES), start=1):
        assert (
            got == expected
        ), f"Line {idx} of {ACCESS_LOG} is incorrect:\n  expected: {expected!r}\n       got: {got!r}"

    # One final sanity check that there are no extra lines beyond the expected 15.
    assert lines == EXPECTED_LOG_LINES, (
        f"{ACCESS_LOG} content does not exactly match the expected "
        "initial 15 log lines."
    )