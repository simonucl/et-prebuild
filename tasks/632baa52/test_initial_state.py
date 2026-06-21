# test_initial_state.py
#
# Pytest suite that verifies the **initial** state of the sandbox
# before the student begins any work.  It checks that:
#
# 1. The /home/user/releases directory exists and is writable.
# 2. The deployment_history_2023-08.log file exists with the exact,
#    byte-for-byte contents and correct permissions.
# 3. The version_frequency_report.tsv file is **not** present yet.
#
# Only stdlib and pytest are used.

import os
import stat
import textwrap
import pytest

RELEASES_DIR = "/home/user/releases"
LOG_FILE = os.path.join(RELEASES_DIR, "deployment_history_2023-08.log")
REPORT_FILE = os.path.join(RELEASES_DIR, "version_frequency_report.tsv")

# Expected exact byte content of the log file, including the single
# trailing LF at the very end.
EXPECTED_LOG_CONTENT = (
    "2023-08-01 04:15:22 myservice:1.4.0\n"
    "2023-08-01 05:00:41 auth:2.3.1\n"
    "2023-08-02 06:32:10 myservice:1.4.0\n"
    "2023-08-02 07:01:11 payments:3.1.0\n"
    "2023-08-03 08:15:22 myservice:1.4.2\n"
    "2023-08-03 09:36:15 auth:2.3.1\n"
    "2023-08-04 10:44:55 payments:3.1.0\n"
    "2023-08-04 11:22:33 payments:3.1.0\n"
    "2023-08-05 12:30:45 myservice:1.4.2\n"
    "2023-08-05 13:11:09 auth:2.3.2\n"
).encode("utf-8")  # Store as bytes for an exact comparison


def _mode(path):
    """Return UNIX permission bits, e.g. 0o644."""
    return stat.S_IMODE(os.stat(path).st_mode)


def test_releases_directory_exists_and_writable():
    assert os.path.isdir(
        RELEASES_DIR
    ), f"Expected directory {RELEASES_DIR!r} to exist but it is missing."
    assert os.access(
        RELEASES_DIR, os.W_OK
    ), f"Directory {RELEASES_DIR!r} is not writable by the current user."


def test_log_file_exists_and_permissions():
    assert os.path.isfile(
        LOG_FILE
    ), f"Expected log file {LOG_FILE!r} to exist but it is missing."
    mode = _mode(LOG_FILE)
    expected_mode = 0o644
    assert (
        mode == expected_mode
    ), f"{LOG_FILE!r} has permissions {oct(mode)}, expected {oct(expected_mode)}."


def test_log_file_exact_contents():
    with open(LOG_FILE, "rb") as fh:
        content = fh.read()
    assert (
        content == EXPECTED_LOG_CONTENT
    ), textwrap.dedent(
        f"""
        Contents of {LOG_FILE!r} do not match the expected initial state.
        --- Expected (byte-for-byte) ---
        {EXPECTED_LOG_CONTENT.decode('utf-8')}
        --- Found ---
        {content.decode('utf-8')}
        """
    ).strip()


def test_report_file_should_not_exist_yet():
    assert not os.path.exists(
        REPORT_FILE
    ), f"{REPORT_FILE!r} already exists, but it should be created by the student."