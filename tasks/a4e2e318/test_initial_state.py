# test_initial_state.py
#
# This test-suite verifies the **initial** filesystem / OS state
# BEFORE the student starts working on the task.
#
# What should already be true:
# 1. Directory  /home/user/logs                exists.
# 2. File       /home/user/logs/local_access.log
#    exists and contains EXACTLY the three Apache log lines given
#    in the public task description (with Unix LF line-endings
#    and a trailing newline after the third line).
#
# What must **not** yet exist:
# 1. File       /home/user/logs/local_ip_hostname_mapping.csv
#
# We also check that a reverse lookup for 127.0.0.1 resolves to
# “localhost”, because the later grading logic relies on that fact.
#
# NOTE:  Nothing in this test ever modifies the filesystem.

import subprocess
from pathlib import Path
import pytest
import textwrap

LOGS_DIR = Path("/home/user/logs")
ACCESS_LOG = LOGS_DIR / "local_access.log"
CSV_OUTPUT = LOGS_DIR / "local_ip_hostname_mapping.csv"

# The exact contents expected inside local_access.log (with LF endings)
EXPECTED_ACCESS_LOG_CONTENT = textwrap.dedent(
    """\
    127.0.0.1 - - [10/Sep/2023:12:00:00 +0000] "GET /index.html HTTP/1.1" 200 1024
    127.0.0.1 - - [10/Sep/2023:12:00:05 +0000] "POST /login HTTP/1.1" 302 512
    127.0.0.1 - - [10/Sep/2023:12:00:10 +0000] "GET /dashboard HTTP/1.1" 200 2048
    """
)


def test_logs_directory_exists():
    assert LOGS_DIR.is_dir(), (
        f"Required directory {LOGS_DIR} is missing. "
        "It must exist before you start."
    )


def test_access_log_exists():
    assert ACCESS_LOG.is_file(), (
        f"The access-log file {ACCESS_LOG} is missing. "
        "It is supposed to be pre-created for you."
    )


def test_access_log_content_exact_match():
    file_bytes = ACCESS_LOG.read_bytes()
    try:
        content = file_bytes.decode("utf-8")
    except UnicodeDecodeError:
        pytest.fail(
            f"The file {ACCESS_LOG} is not valid UTF-8 encoded text."
        )

    # Ensure the file ends with a single trailing LF (\n)
    assert content.endswith("\n"), (
        f"The file {ACCESS_LOG} must end with a single trailing newline."
    )

    assert content == EXPECTED_ACCESS_LOG_CONTENT, (
        f"The file {ACCESS_LOG} does not contain the expected three log lines.\n"
        "If the file was changed accidentally, restore it to exactly:\n"
        f"{EXPECTED_ACCESS_LOG_CONTENT!r}"
    )


def test_output_csv_not_present_yet():
    assert not CSV_OUTPUT.exists(), (
        f"The output file {CSV_OUTPUT} already exists, but it should be created "
        "only AFTER you complete the task."
    )


def test_reverse_lookup_127_0_0_1_resolves_to_localhost():
    """
    The later grading script relies on 127.0.0.1 → localhost reverse lookup.
    Make sure that the current system is configured accordingly.
    """
    try:
        result = subprocess.run(
            ["getent", "hosts", "127.0.0.1"],
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        pytest.skip(
            "'getent' command not found; cannot verify reverse lookup. "
            "This shouldn't happen on a standard Debian/Ubuntu container."
        )

    stdout = result.stdout.strip()
    assert stdout, "No output from 'getent hosts 127.0.0.1' ― resolver misconfigured."
    columns = stdout.split()
    hostname_present = any(col.lower() == "localhost" for col in columns[1:])
    assert hostname_present, (
        "Reverse lookup for 127.0.0.1 does not return 'localhost'.\n"
        "The /etc/hosts file (or DNS resolver) must map 127.0.0.1 to localhost."
    )