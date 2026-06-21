# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / file-system
# state **before** the student runs any commands for the “ping report”
# clean-up task.
#
# What we verify (truth values from the task description):
#   • Directory  : /home/user/network      → must exist and be writable.
#   • Log file   : /home/user/network/ping_report.log
#                 – must exist, be a regular file, and contain the exact
#                   kinds of lines described in the prompt.
#
# We deliberately DO NOT test for the presence of any *output* artefacts
# (`successful_ips.txt`, etc.); those will be created by the student.
#
# Only the Python stdlib + pytest are used.

import os
import stat
from pathlib import Path

import pytest

NETWORK_DIR = Path("/home/user/network")
LOG_FILE = NETWORK_DIR / "ping_report.log"


def read_log():
    """Read the entire log file and return its contents as a string.

    This helper centralises the file‐reading logic so that each test can
    focus on its specific assertion.
    """
    try:
        with LOG_FILE.open("r", encoding="utf-8") as fp:
            return fp.read()
    except FileNotFoundError as exc:  # pragma: no cover  (will surface anyway)
        pytest.fail(f"Required log file is missing: {LOG_FILE}", pytrace=False)


def test_network_directory_exists_and_is_writable():
    assert NETWORK_DIR.exists(), f"Directory {NETWORK_DIR} is missing."
    assert NETWORK_DIR.is_dir(), f"{NETWORK_DIR} exists but is not a directory."

    # Verify write permission for the current (unprivileged) user.
    mode = NETWORK_DIR.stat().st_mode
    writable = bool(mode & stat.S_IWUSR)
    assert writable, f"Directory {NETWORK_DIR} is not writable by the current user."


def test_ping_report_log_file_exists_and_is_regular_file():
    assert LOG_FILE.exists(), f"Log file {LOG_FILE} is missing."
    assert LOG_FILE.is_file(), f"{LOG_FILE} exists but is not a regular file."

    # A rough size check: should be non-empty and not absurdly large.
    size = LOG_FILE.stat().st_size
    assert 100 <= size <= 10_000, (
        f"Log file size looks suspicious ({size} bytes). "
        "Expected roughly ~1.2 KB."
    )


def test_log_file_has_unix_line_endings_only():
    data = read_log()
    assert "\r" not in data, (
        f"Log file {LOG_FILE} contains Windows (CRLF) line endings; "
        "expected Unix LF only."
    )


def test_log_file_terminates_with_single_newline():
    data = read_log()
    assert data.endswith("\n"), (
        f"Log file {LOG_FILE} must end with a single LF newline."
    )
    assert not data.endswith("\n\n"), (
        f"Log file {LOG_FILE} ends with multiple blank lines; "
        "should terminate with exactly one newline."
    )


@pytest.mark.parametrize(
    "needle",
    [
        # Successful replies that must be present.
        "64 bytes from 8.8.8.8:",
        "64 bytes from 1.1.1.1:",
    ],
)
def test_log_contains_required_success_lines(needle):
    data = read_log()
    assert needle in data, (
        f"Expected successful reply line containing "
        f"'{needle}' in {LOG_FILE}, but it was not found."
    )


def test_log_does_not_contain_false_positive_success_for_invalid_host():
    data = read_log()
    # 203.0.113.10 is in the log but only in the PING header; there must be
    # no “64 bytes from …” success lines for it.
    assert "64 bytes from 203.0.113.10:" not in data, (
        "Log file incorrectly contains a successful reply line for "
        "203.0.113.10, which should only have timeouts."
    )


def test_log_contains_expected_timeout_and_unreachable_lines():
    data = read_log()
    assert "Request timeout for icmp_seq" in data, (
        "Expected at least one timeout line in the log, but none were found."
    )
    assert "Destination Host Unreachable" in data, (
        "Expected a 'Destination Host Unreachable' line in the log, "
        "but none were found."
    )