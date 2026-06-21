# test_initial_state.py
#
# This test-suite verifies the **initial** state of the operating system
# before the student starts working on the assignment.  It purposely checks
# only for the things that must already exist, and equally confirms that
# nothing that belongs to the *solution* is present yet.
#
# – Exactly one access log must exist at /home/user/logs/access.log.
# – The webstats workspace (/home/user/webstats) must NOT exist yet.
# – The log file must contain the precise 27 lines given in the task
#   description (including their trailing newline characters).

import os
import hashlib
import pytest


ACCESS_LOG = "/home/user/logs/access.log"
WEBSTATS_DIR = "/home/user/webstats"


@pytest.fixture(scope="module")
def access_log_lines():
    """Read all lines of the access log in UTF-8."""
    if not os.path.isfile(ACCESS_LOG):
        pytest.skip(f"{ACCESS_LOG} is missing – cannot perform content checks")

    with open(ACCESS_LOG, "r", encoding="utf-8") as fh:
        return fh.readlines()


def test_directory_layout():
    """Basic directory / file checks."""
    assert os.path.isdir("/home/user"), "Home directory /home/user should exist"
    assert os.path.isdir(
        "/home/user/logs"
    ), "Logs directory /home/user/logs should exist"

    assert os.path.isfile(
        ACCESS_LOG
    ), f"Expected access log at {ACCESS_LOG} – file is missing"

    # The solution directory must NOT exist yet.
    assert not os.path.exists(
        WEBSTATS_DIR
    ), f"{WEBSTATS_DIR} should NOT exist before the task is attempted"


def test_access_log_line_count(access_log_lines):
    """Ensure the file has exactly 27 lines."""
    assert (
        len(access_log_lines) == 27
    ), f"{ACCESS_LOG} should have 27 lines, found {len(access_log_lines)}"


def test_access_log_exact_content(access_log_lines):
    """Compare the full log file with the reference lines."""
    expected_lines = [
        '192.168.0.10 - - [12/Mar/2023:10:15:01 +0000] "GET /index.html HTTP/1.1" 200 1024 "-" "Mozilla/5.0"\n',
        '192.168.0.10 - - [12/Mar/2023:10:15:03 +0000] "GET /old-page.php HTTP/1.1" 404 512 "-" "Mozilla/5.0"\n',
        '192.168.0.10 - - [12/Mar/2023:10:15:05 +0000] "POST /api/data HTTP/1.1" 200 2048 "-" "curl/7.81.0"\n',
        '192.168.0.10 - - [12/Mar/2023:10:15:07 +0000] "GET /about.html HTTP/1.1" 200 1536 "-" "Mozilla/5.0"\n',
        '192.168.0.10 - - [12/Mar/2023:10:15:09 +0000] "POST /process.php HTTP/1.1" 404 256 "-" "curl/7.81.0"\n',
        '192.168.0.10 - - [12/Mar/2023:10:15:11 +0000] "GET /styles.css HTTP/1.1" 200 4096 "-" "Mozilla/5.0"\n',
        '192.168.0.10 - - [12/Mar/2023:10:15:13 +0000] "POST /submit-form HTTP/1.1" 200 1024 "-" "curl/7.81.0"\n',
        '192.168.0.10 - - [12/Mar/2023:10:15:15 +0000] "GET /missing.html HTTP/1.1" 404 256 "-" "Mozilla/5.0"\n',
        '172.16.0.5 - - [12/Mar/2023:11:20:01 +0000] "GET /home HTTP/1.1" 200 3072 "-" "Mozilla/5.0"\n',
        '172.16.0.5 - - [12/Mar/2023:11:20:03 +0000] "GET /data HTTP/1.1" 200 1024 "-" "Mozilla/5.0"\n',
        '172.16.0.5 - - [12/Mar/2023:11:20:05 +0000] "POST /login HTTP/1.1" 200 2048 "-" "curl/7.81.0"\n',
        '172.16.0.5 - - [12/Mar/2023:11:20:07 +0000] "POST /save HTTP/1.1" 200 1024 "-" "curl/7.81.0"\n',
        '172.16.0.5 - - [12/Mar/2023:11:20:09 +0000] "POST /login.php HTTP/1.1" 404 128 "-" "curl/7.81.0"\n',
        '172.16.0.5 - - [12/Mar/2023:11:20:11 +0000] "GET /error HTTP/1.1" 500 512 "-" "Mozilla/5.0"\n',
        '10.0.0.3 - - [12/Mar/2023:12:05:01 +0000] "GET /dashboard HTTP/1.1" 200 4096 "-" "Mozilla/5.0"\n',
        '10.0.0.3 - - [12/Mar/2023:12:05:03 +0000] "GET /report HTTP/1.1" 200 2048 "-" "Mozilla/5.0"\n',
        '10.0.0.3 - - [12/Mar/2023:12:05:05 +0000] "GET /admin.php HTTP/1.1" 404 512 "-" "Mozilla/5.0"\n',
        '10.0.0.3 - - [12/Mar/2023:12:05:07 +0000] "GET /stats HTTP/1.1" 200 3072 "-" "Mozilla/5.0"\n',
        '10.0.0.3 - - [12/Mar/2023:12:05:09 +0000] "GET /server-error HTTP/1.1" 500 256 "-" "Mozilla/5.0"\n',
        '203.0.113.55 - - [12/Mar/2023:13:40:01 +0000] "GET /contact.php HTTP/1.1" 404 512 "-" "Mozilla/5.0"\n',
        '203.0.113.55 - - [12/Mar/2023:13:40:03 +0000] "GET /shop HTTP/1.1" 200 2048 "-" "Mozilla/5.0"\n',
        '203.0.113.55 - - [12/Mar/2023:13:40:05 +0000] "GET /product HTTP/1.1" 200 1536 "-" "Mozilla/5.0"\n',
        '203.0.113.55 - - [12/Mar/2023:13:40:07 +0000] "GET /pricing HTTP/1.1" 200 1024 "-" "Mozilla/5.0"\n',
        '198.51.100.77 - - [12/Mar/2023:14:10:01 +0000] "POST /signup HTTP/1.1" 200 2048 "-" "curl/7.81.0"\n',
        '198.51.100.77 - - [12/Mar/2023:14:10:03 +0000] "POST /preferences HTTP/1.1" 200 1024 "-" "curl/7.81.0"\n',
        '198.51.100.77 - - [12/Mar/2023:14:10:05 +0000] "POST /signup.php HTTP/1.1" 404 128 "-" "curl/7.81.0"\n',
        '127.0.0.1 - - [12/Mar/2023:14:55:01 +0000] "GET /health HTTP/1.1" 200 64 "-" "curl/7.81.0"\n',
    ]

    assert (
        access_log_lines == expected_lines
    ), "The contents of access.log do not match the expected initial data set"

    # Extra safety: make sure the very last byte of the file is indeed '\n'
    assert access_log_lines[-1].endswith(
        "\n"
    ), "The last line of access.log must be newline-terminated"