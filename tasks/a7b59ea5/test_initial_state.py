# test_initial_state.py
"""
Pytest suite that validates the expected *initial* state of the operating system /
filesystem for the “backup-operator” exercise.

The tests cover:
1. Existence of all required directories and files.
2. Exact contents of source data, cron specification, systemd unit files.
3. Executability of the backup script.
4. Log file contains at least one correctly-formatted entry.
5. Destination copy of important.txt is byte-identical to the source.
"""

import os
import stat
import re
import filecmp
import pytest

# --------------------------------------------------------------------------- #
# Constants – all paths that must exist
# --------------------------------------------------------------------------- #
HOME = "/home/user"

SRC_DIR       = f"{HOME}/backup_test/source"
SRC_FILE      = f"{SRC_DIR}/important.txt"

DST_DIR       = f"{HOME}/backup_test/backup"
DST_FILE      = f"{DST_DIR}/important.txt"

SCRIPTS_DIR   = f"{HOME}/backup_scripts"
SCRIPT_FILE   = f"{SCRIPTS_DIR}/backup_once.sh"
LOG_FILE      = f"{SCRIPTS_DIR}/backup.log"
CRON_FILE     = f"{SCRIPTS_DIR}/backup.cron"

SYSTEMD_DIR   = f"{HOME}/.config/systemd/user"
SERVICE_FILE  = f"{SYSTEMD_DIR}/backup_once.service"
TIMER_FILE    = f"{SYSTEMD_DIR}/backup_once.timer"

# Expected static file bodies
EXPECTED_SOURCE_CONTENT = "Important data v1\n"

EXPECTED_CRON_LINE = "17 2 * * * /home/user/backup_scripts/backup_once.sh\n"

EXPECTED_SERVICE_CONTENT = (
    "[Unit]\n"
    "Description=One-off user backup\n"
    "\n"
    "[Service]\n"
    "Type=oneshot\n"
    "ExecStart=/home/user/backup_scripts/backup_once.sh\n"
)

EXPECTED_TIMER_CONTENT = (
    "[Unit]\n"
    "Description=Run user backup 5 minutes after boot\n"
    "\n"
    "[Timer]\n"
    "OnBootSec=5min\n"
    "Unit=backup_once.service\n"
    "\n"
    "[Install]\n"
    "WantedBy=default.target\n"
)

# Regex for a valid log line
LOG_LINE_REGEX = re.compile(
    r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T"           # Date
    r"[0-9]{2}:[0-9]{2}:[0-9]{2}"             # Time
    r"(?:[+-][0-9]{2}:[0-9]{2}|Z)"            # TZ offset or Z
    r" : Backed up important.txt$"            # Literal trailer
)


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def _assert_exists(path: str, is_dir: bool = False):
    """Assert that `path` exists (and is a dir if requested)."""
    if not os.path.exists(path):
        pytest.fail(f"Expected {'directory' if is_dir else 'file'} at {path} is missing")
    if is_dir and not os.path.isdir(path):
        pytest.fail(f"Expected directory at {path} but found a non-directory")
    if not is_dir and not os.path.isfile(path):
        pytest.fail(f"Expected file at {path} but found a non-regular file")


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_required_directories_exist():
    for directory in (SRC_DIR, DST_DIR, SCRIPTS_DIR, SYSTEMD_DIR):
        _assert_exists(directory, is_dir=True)


def test_source_file_content():
    _assert_exists(SRC_FILE)
    with open(SRC_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == EXPECTED_SOURCE_CONTENT, (
        f"{SRC_FILE} must contain exactly one line "
        f'\'{EXPECTED_SOURCE_CONTENT.rstrip()}\' (with trailing newline)'
    )


def test_destination_copy_is_identical():
    _assert_exists(DST_FILE)
    identical = filecmp.cmp(SRC_FILE, DST_FILE, shallow=False)
    assert identical, "Source and destination important.txt files differ"


def test_backup_script_is_executable():
    _assert_exists(SCRIPT_FILE)
    st = os.stat(SCRIPT_FILE)
    is_executable = bool(st.st_mode & stat.S_IXUSR)
    assert is_executable, f"{SCRIPT_FILE} must have the user-executable bit set"
    assert os.access(SCRIPT_FILE, os.X_OK), f"{SCRIPT_FILE} is not executable by the current user"


def test_log_file_contains_valid_entry():
    _assert_exists(LOG_FILE)
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lines = [ln.rstrip("\n") for ln in f]
    assert lines, f"{LOG_FILE} is empty; expected at least one log line"
    if not any(LOG_LINE_REGEX.match(ln) for ln in lines):
        pytest.fail(
            f"{LOG_FILE} does not contain a line matching the required format:\n"
            "YYYY-MM-DDThh:mm:ss±hh:mm : Backed up important.txt"
        )


def test_cron_file_contents_exact():
    _assert_exists(CRON_FILE)
    with open(CRON_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    assert len(lines) == 1, f"{CRON_FILE} must contain exactly one line"
    assert lines[0] == EXPECTED_CRON_LINE, (
        f"{CRON_FILE} content mismatch.\n"
        f"Expected: {EXPECTED_CRON_LINE!r}\n"
        f"Found:    {lines[0]!r}"
    )


def test_service_unit_contents_exact():
    _assert_exists(SERVICE_FILE)
    with open(SERVICE_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    assert content == EXPECTED_SERVICE_CONTENT, (
        f"{SERVICE_FILE} content mismatch.\n"
        "File must match the specification exactly."
    )


def test_timer_unit_contents_exact():
    _assert_exists(TIMER_FILE)
    with open(TIMER_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    assert content == EXPECTED_TIMER_CONTENT, (
        f"{TIMER_FILE} content mismatch.\n"
        "File must match the specification exactly."
    )