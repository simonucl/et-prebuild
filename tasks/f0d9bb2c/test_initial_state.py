# test_initial_state.py
#
# Pytest suite that validates the OS / filesystem **before** the student
# performs any action.  It ensures that the starting conditions described in
# the assignment are present and correct.

import os
import stat
import textwrap
import pytest

LOGS_DIR = "/home/user/logs"
ACCESS_LOG = os.path.join(LOGS_DIR, "webserver_access.log")
ERRORS_LOG = os.path.join(LOGS_DIR, "errors_only.log")


@pytest.fixture(scope="module")
def expected_access_log_content():
    """
    Return the exact, canonical content that must be present in
    /home/user/logs/webserver_access.log *including* the trailing LF.
    """
    content = textwrap.dedent(
        """\
        127.0.0.1 - - [10/Oct/2022:13:55:36 +0000] "GET /index.html HTTP/1.1" 200 1024 "-" "Mozilla/5.0"
        192.168.1.10 - - [10/Oct/2022:14:00:01 +0000] "POST /login HTTP/1.1" 302 512 "-" "Mozilla/5.0"
        10.0.0.5 - - [10/Oct/2022:14:02:16 +0000] "GET /doesnotexist HTTP/1.1" 404 256 "-" "Mozilla/5.0"
        127.0.0.1 - - [10/Oct/2022:14:05:45 +0000] "GET /api/data HTTP/1.1" 500 128 "-" "curl/7.68.0"
        203.0.113.55 - - [10/Oct/2022:14:06:12 +0000] "PUT /api/update HTTP/1.1" 503 64 "-" "Python-requests/2.25.1"
        192.0.2.44 - - [10/Oct/2022:14:07:30 +0000] "DELETE /api/delete HTTP/1.1" 204 0 "-" "Mozilla/5.0"
        198.51.100.23 - - [10/Oct/2022:14:08:59 +0000] "GET /reports HTTP/1.1" 504 32 "-" "Mozilla/5.0"
        203.0.113.77 - - [10/Oct/2022:14:10:42 +0000] "GET /admin HTTP/1.1" 403 128 "-" "Mozilla/5.0"
        192.168.1.15 - - [10/Oct/2022:14:12:03 +0000] "POST /submit HTTP/1.1" 201 256 "-" "curl/7.68.0"
        10.1.1.1 - - [10/Oct/2022:14:13:27 +0000] "GET /status HTTP/1.1" 502 16 "-" "Mozilla/5.0"
        """
    )
    # Ensure the dedented text ends with exactly one LF
    if not content.endswith("\n"):
        content += "\n"
    return content


def test_logs_directory_exists_and_permissions():
    """The /home/user/logs directory must exist and be a directory."""
    assert os.path.isdir(LOGS_DIR), (
        f"Expected directory {LOGS_DIR!r} to exist, but it is missing or "
        "is not a directory."
    )
    # Basic sanity-check on permissions: directory must be world-readable (0755 typical)
    mode = stat.S_IMODE(os.stat(LOGS_DIR).st_mode)
    assert mode & stat.S_IROTH, (
        f"Directory {LOGS_DIR!r} should be world-readable; "
        f"current mode is {oct(mode)}."
    )


def test_access_log_exists(expected_access_log_content):
    """The access log must exist at the exact path before any action is taken."""
    assert os.path.isfile(ACCESS_LOG), (
        f"Expected access log file {ACCESS_LOG!r} to exist, but it is missing."
    )
    # Quick size sanity-check: should be non-empty
    size = os.path.getsize(ACCESS_LOG)
    assert size > 0, f"The access log {ACCESS_LOG!r} is empty (size 0)."


def test_access_log_exact_content(expected_access_log_content):
    """
    Verify that the access log content is *exactly* as specified,
    including order and trailing newlines.
    """
    with open(ACCESS_LOG, "r", encoding="utf-8") as fp:
        actual = fp.read()

    assert actual == expected_access_log_content, (
        "The content of /home/user/logs/webserver_access.log does not match the "
        "expected initial state.  If you modified the file, restore it to its "
        "original state before proceeding.\n"
        "\n"
        "---- Expected ----\n"
        f"{expected_access_log_content}"
        "---- Actual ----\n"
        f"{actual}"
    )

    # Additional structural checks
    lines = actual.splitlines(keepends=False)
    assert len(lines) == 10, (
        f"Expected 10 lines in the access log, found {len(lines)}."
    )
    # Ensure no CRLF line endings slipped in
    assert all("\r" not in line for line in lines), (
        "Carriage-return characters (CR) detected in access log; "
        "file should use UNIX LF line endings only."
    )


def test_errors_log_does_not_exist_yet():
    """
    /home/user/logs/errors_only.log must NOT exist before the student
    runs their single command.
    """
    assert not os.path.exists(ERRORS_LOG), (
        f"File {ERRORS_LOG!r} already exists, but it should not be present "
        "before the task is executed.  Please remove it before starting."
    )