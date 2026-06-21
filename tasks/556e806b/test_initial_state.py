# test_initial_state.py
#
# Pytest suite that validates the initial filesystem state **before** the
# student’s solution is applied.  It checks only the prerequisites that must
# already exist:
#
#   1. The directory /home/user/logs  (permissions 755)
#   2. The file     /home/user/logs/webserver.log  (permissions 644)
#      with the exact expected contents.
#
# It intentionally does NOT look for any files the student is supposed to
# create later (e.g. /home/user/analyze_errors.sh or 404_report.log).

import os
import stat
import textwrap
import pytest

LOG_DIR = "/home/user/logs"
LOG_FILE = os.path.join(LOG_DIR, "webserver.log")


def _mode(path):
    "Return the permission bits (e.g., 0o755) for a filesystem object."
    return stat.S_IMODE(os.stat(path).st_mode)


def test_log_directory_exists_and_has_correct_permissions():
    assert os.path.isdir(LOG_DIR), (
        f"Required directory missing: {LOG_DIR!r}. "
        "It must exist before the task is started."
    )
    expected_mode = 0o755
    actual_mode = _mode(LOG_DIR)
    assert actual_mode == expected_mode, (
        f"{LOG_DIR!r} has permissions {oct(actual_mode)}, "
        f"expected {oct(expected_mode)}."
    )


def test_webserver_log_exists_and_has_correct_permissions():
    assert os.path.isfile(LOG_FILE), (
        f"Required log file missing: {LOG_FILE!r}. "
        "It must be provided to the student as input."
    )
    expected_mode = 0o644
    actual_mode = _mode(LOG_FILE)
    assert actual_mode == expected_mode, (
        f"{LOG_FILE!r} has permissions {oct(actual_mode)}, "
        f"expected {oct(expected_mode)}."
    )


@pytest.fixture(scope="module")
def expected_log_contents():
    """
    The exact contents the webserver.log must contain before the student's script
    runs.  A trailing newline after the last line is allowed but not required.
    """
    return textwrap.dedent(
        """\
        127.0.0.1 - - [10/Oct/2023:13:55:36 +0000] "GET /index.html HTTP/1.1" 200 1024
        192.168.1.10 - - [10/Oct/2023:14:01:02 +0000] "GET /not-found HTTP/1.1" 404 512
        203.0.113.5 - - [10/Oct/2023:14:03:17 +0000] "POST /login HTTP/1.1" 302 214
        198.51.100.23 - - [10/Oct/2023:14:06:44 +0000] "GET /old-page HTTP/1.1" 404 198
        192.0.2.77 - - [10/Oct/2023:14:09:58 +0000] "GET /favicon.ico HTTP/1.1" 200 543
        192.168.1.10 - - [10/Oct/2023:14:12:11 +0000] "GET /robots.txt HTTP/1.1" 404 87
        203.0.113.5 - - [10/Oct/2023:14:14:29 +0000] "GET /missing.jpg HTTP/1.1" 404 64
        198.51.100.23 - - [10/Oct/2023:14:17:03 +0000] "GET /archive.zip HTTP/1.1" 200 3245
        192.0.2.77 - - [10/Oct/2023:14:19:43 +0000] "HEAD /secret HTTP/1.1" 404 0
        127.0.0.1 - - [10/Oct/2023:14:22:55 +0000] "GET /index.html HTTP/1.1" 200 1024
        """
    )


def test_webserver_log_contents(expected_log_contents):
    assert os.path.isfile(LOG_FILE), "webserver.log is missing."

    with open(LOG_FILE, "r", encoding="utf-8") as fh:
        actual = fh.read()

    # Normalize by stripping a single trailing newline from both sides so that
    # we accept files that either include or omit the final newline character.
    assert actual.rstrip("\n") == expected_log_contents.rstrip("\n"), (
        f"The contents of {LOG_FILE!r} do not match the expected initial state."
    )