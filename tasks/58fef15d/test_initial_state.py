# test_initial_state.py
#
# Pytest suite that verifies the **initial** state of the operating-system
# before the student starts working on the assignment.  It checks that:
#
# 1. The working directory /home/user/log-analysis exists.
# 2. The file /home/user/log-analysis/sample_access.log exists **unchanged**
#    and contains exactly the 15 log-lines provided by Operations.
# 3. The report file that the student will have to create
#    (/home/user/log-analysis/ip_frequency_report.txt) does NOT exist yet.
#
# If any of these assertions fail, the error message should guide the
# student towards what is missing or out of place.
#
# Only stdlib + pytest are used.

import os
from pathlib import Path

WORKDIR = Path("/home/user/log-analysis")
ACCESS_LOG = WORKDIR / "sample_access.log"
REPORT_FILE = WORKDIR / "ip_frequency_report.txt"

EXPECTED_CONTENT = (
    "192.168.1.10 - - [10/May/2024:10:00:01 +0000] \"GET /index.html HTTP/1.1\" 200 1024\n"
    "203.0.113.5 - - [10/May/2024:10:00:03 +0000] \"POST /login HTTP/1.1\" 302 512\n"
    "192.168.1.10 - - [10/May/2024:10:00:04 +0000] \"GET /dashboard HTTP/1.1\" 200 2048\n"
    "198.51.100.23 - - [10/May/2024:10:00:05 +0000] \"GET /index.html HTTP/1.1\" 200 1024\n"
    "203.0.113.5 - - [10/May/2024:10:00:06 +0000] \"GET /profile HTTP/1.1\" 200 1024\n"
    "192.0.2.45 - - [10/May/2024:10:00:07 +0000] \"GET /index.html HTTP/1.1\" 404 256\n"
    "192.168.1.10 - - [10/May/2024:10:00:08 +0000] \"GET /settings HTTP/1.1\" 200 1024\n"
    "198.51.100.23 - - [10/May/2024:10:00:09 +0000] \"GET /contact HTTP/1.1\" 200 512\n"
    "203.0.113.5 - - [10/May/2024:10:00:10 +0000] \"GET /dashboard HTTP/1.1\" 200 1024\n"
    "203.0.113.5 - - [10/May/2024:10:00:11 +0000] \"GET /logout HTTP/1.1\" 200 256\n"
    "192.0.2.45 - - [10/May/2024:10:00:12 +0000] \"POST /login HTTP/1.1\" 302 512\n"
    "192.0.2.45 - - [10/May/2024:10:00:13 +0000] \"GET /home HTTP/1.1\" 200 1024\n"
    "192.168.1.10 - - [10/May/2024:10:00:14 +0000] \"GET /logout HTTP/1.1\" 200 256\n"
    "198.51.100.23 - - [10/May/2024:10:00:15 +0000] \"GET /settings HTTP/1.1\" 200 1024\n"
    "192.0.2.45 - - [10/May/2024:10:00:16 +0000] \"GET /contact HTTP/1.1\" 200 512\n"
)

def test_working_directory_exists():
    assert WORKDIR.exists(), (
        f"Required directory {WORKDIR} is missing. "
        "Create it before proceeding with the task."
    )
    assert WORKDIR.is_dir(), f"{WORKDIR} exists but is not a directory."

def test_access_log_present_and_correct():
    assert ACCESS_LOG.exists(), (
        f"The access-log file {ACCESS_LOG} is missing. "
        "It should have been provided by Operations; do not delete or move it."
    )
    assert ACCESS_LOG.is_file(), f"{ACCESS_LOG} exists but is not a regular file."

    with ACCESS_LOG.open("r", encoding="utf-8") as fh:
        content = fh.read()

    # Verify byte-for-byte equality with the expected template.
    assert content == EXPECTED_CONTENT, (
        f"The file {ACCESS_LOG} does not match the expected content.\n\n"
        "Possible reasons:\n"
        "  * The file was modified.\n"
        "  * Extra or missing whitespace/newlines.\n"
        "  * Wrong number of lines.\n\n"
        "Restore the original file so that it contains exactly 15 lines "
        "with the content supplied by Operations."
    )

def test_report_file_absent_initially():
    assert not REPORT_FILE.exists(), (
        f"The file {REPORT_FILE} should NOT exist before you run your commands. "
        "Create it only after computing the IP frequency report."
    )