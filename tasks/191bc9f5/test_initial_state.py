# test_initial_state.py
#
# This test-suite validates the **initial** state of the OS / filesystem
# BEFORE the student’s solution is executed.  It checks that only the
# source log is present and that the output directory / files do **not**
# yet exist.
#
# Rules enforced (taken from the task description):
#   • /home/user/network exists               – permissions 0755
#   • /home/user/network/access.log exists    – permissions 0644, exact contents
#   • /home/user/analysis/dns_summary.csv MUST NOT exist yet
#
# Any deviation will cause the test-suite to fail with an explicit and
# helpful assertion message.
#
# Only stdlib + pytest are used.

import os
import stat
import pytest

NETWORK_DIR = "/home/user/network"
ACCESS_LOG = os.path.join(NETWORK_DIR, "access.log")
ANALYSIS_DIR = "/home/user/analysis"
OUTPUT_CSV = os.path.join(ANALYSIS_DIR, "dns_summary.csv")

EXPECTED_ACCESS_LOG_CONTENT = (
    b'10.0.0.15 - - [12/Dec/2023:10:15:21 +0000] "GET http://localhost/index.html HTTP/1.1" 200 512\n'
    b'10.0.0.15 - - [12/Dec/2023:10:15:22 +0000] "GET http://example.com/assets/logo.png HTTP/1.1" 200 1024\n'
    b'10.0.0.15 - - [12/Dec/2023:10:15:25 +0000] "GET http://nonexistent.domain.tld/register HTTP/1.1" 404 123\n'
)


def _mode(path: str) -> int:
    """
    Return the permission bits (e.g. 0o755) of a given path.
    """
    return stat.S_IMODE(os.stat(path).st_mode)


def test_network_directory_exists_and_perms():
    assert os.path.isdir(NETWORK_DIR), (
        f"Expected directory {NETWORK_DIR} to exist, but it is missing "
        f"or not a directory."
    )
    perms = _mode(NETWORK_DIR)
    expected = 0o755
    assert perms == expected, (
        f"Directory {NETWORK_DIR} must have permissions {oct(expected)}, "
        f"found {oct(perms)} instead."
    )


def test_access_log_exists_and_perms():
    assert os.path.isfile(ACCESS_LOG), (
        f"Expected access log {ACCESS_LOG} to exist, but it does not."
    )
    perms = _mode(ACCESS_LOG)
    expected = 0o644
    assert perms == expected, (
        f"File {ACCESS_LOG} must have permissions {oct(expected)}, "
        f"found {oct(perms)} instead."
    )


def test_access_log_exact_contents():
    with open(ACCESS_LOG, "rb") as fh:
        data = fh.read()

    assert data == EXPECTED_ACCESS_LOG_CONTENT, (
        f"The contents of {ACCESS_LOG} do not match the expected three-line "
        "HTTP access log provided by the exercise specification.  "
        "Ensure the file has not been modified."
    )


def test_output_files_absent_initially():
    """
    Before the student runs their solution, the analysis directory or the
    CSV report must **not** exist (the student is responsible for creating
    them later).
    """
    assert not os.path.exists(OUTPUT_CSV), (
        f"Output file {OUTPUT_CSV} already exists, but it should NOT be "
        "present before the student runs their script."
    )