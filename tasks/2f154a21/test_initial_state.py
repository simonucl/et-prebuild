# test_initial_state.py
#
# This pytest suite validates that the machine is in the correct *initial*
# state before the student performs any actions for the “tinyftp” task.
#
# The tests assert:
#   • Required directories and the main configuration & log files exist.
#   • The configuration file is still on the default setting
#     (`log-level=INFO`) and is byte-for-byte what we expect.
#   • No backup, filtered-debug log, or summary file exists yet.
#   • The main log contains the expected DEBUG lines in the correct order.
#
# Only the Python stdlib and pytest are used.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
TINYFTP_DIR = HOME / "tinyftp"
LOG_DIR = HOME / "logs"

CONF_FILE = TINYFTP_DIR / "tinyftp.conf"
CONF_BAK = TINYFTP_DIR / "tinyftp.conf.bak"

MAIN_LOG = LOG_DIR / "tinyftp.log"
DEBUG_LOG = LOG_DIR / "tinyftp_debug.log"
SUMMARY_LOG = LOG_DIR / "tinyftp_debug_summary.log"


@pytest.fixture(scope="module")
def config_contents():
    """Return the config file split into individual (stripped) lines."""
    if not CONF_FILE.is_file():
        pytest.fail(f"Expected config file not found: {CONF_FILE}")
    data = CONF_FILE.read_text(encoding="utf-8")
    return data.splitlines(keepends=False), data.encode()


def test_required_directories_exist():
    for directory in (TINYFTP_DIR, LOG_DIR):
        assert directory.is_dir(), (
            f"Required directory missing: {directory}"
        )


def test_config_file_contents(config_contents):
    lines, raw_bytes = config_contents
    expected_lines = [
        "# tinyftp configuration",
        "port=2121",
        "log-level=INFO",
    ]

    assert lines == expected_lines, (
        f"{CONF_FILE} does not match the required initial contents.\n"
        f"Expected:\n{os.linesep.join(expected_lines)}\n\n"
        f"Actual:\n{os.linesep.join(lines)}"
    )

    # Ensure file ends with a single newline byte (Unix LF).
    assert raw_bytes.endswith(b"\n"), (
        f"{CONF_FILE} must end with exactly one newline character (\\n)."
    )
    # And *only* one newline at the end.
    assert not raw_bytes.endswith(b"\n\n"), (
        f"{CONF_FILE} appears to have more than one trailing blank line."
    )


def test_backup_file_is_absent():
    assert not CONF_BAK.exists(), (
        f"Backup file {CONF_BAK} should NOT exist yet."
    )


def test_filtered_debug_and_summary_logs_absent():
    for path in (DEBUG_LOG, SUMMARY_LOG):
        assert not path.exists(), (
            f"{path} should NOT exist before the task is performed."
        )


def test_main_log_contains_expected_debug_lines():
    assert MAIN_LOG.is_file(), f"Main log file missing: {MAIN_LOG}"

    log_lines = MAIN_LOG.read_text(encoding="utf-8").splitlines()

    expected_debug_lines = [
        "2023-09-01 12:01:00 DEBUG: Connection from 192.168.1.10 accepted",
        "2023-09-01 12:03:00 DEBUG: Connection closed for 192.168.1.10",
    ]

    for line in expected_debug_lines:
        assert line in log_lines, (
            f"Expected DEBUG line not found in {MAIN_LOG}:\n{line}"
        )

    # Ensure ordering of DEBUG lines is preserved in the source log.
    indices = [log_lines.index(line) for line in expected_debug_lines]
    assert indices == sorted(indices), (
        f"DEBUG lines in {MAIN_LOG} are not in the expected order."
    )