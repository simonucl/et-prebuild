# test_initial_state.py
#
# Pytest suite that validates the initial state of the operating-system /
# file-system environment *before* the student starts solving ticket #5678.
#
# The expectations below **must** hold prior to any user action:
#
# 1. File /home/user/tickets/ticket_5678/app.conf already exists.
# 2. The INI file contains a [Network] section with key ``port`` set to 8080
#    (spacing around = is not significant).  It must *not* yet contain 9090.
# 3. Directory /home/user/ticket_logs/ exists and is writable, but the file
#    /home/user/ticket_logs/ticket_5678_resolution.log must **not** exist yet.
# 4. Parent directories /home/user/tickets/ and /home/user/tickets/ticket_5678/
#    exist and are writable.
#
# Only stdlib + pytest are used.

import os
import stat
import configparser
import pytest

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

APP_CONF_PATH = "/home/user/tickets/ticket_5678/app.conf"
TICKETS_DIR = "/home/user/tickets"
TICKET_DIR = "/home/user/tickets/ticket_5678"
LOGS_DIR = "/home/user/ticket_logs"
RESOLUTION_LOG = "/home/user/ticket_logs/ticket_5678_resolution.log"


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _is_writable(path: str) -> bool:
    """
    Return True if `path` is writable by the current real UID/GID.
    Works for both files and directories.
    """
    return os.access(path, os.W_OK)


def _read_ini_file(path: str) -> configparser.ConfigParser:
    """
    Return a ConfigParser object loaded from `path`.  We preserve case
    sensitivity of keys to match expectations exactly.
    """
    parser = configparser.ConfigParser()
    parser.optionxform = str  # keep case
    with open(path, "r", encoding="utf-8") as fp:
        parser.read_file(fp)
    return parser


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_directories_exist_and_writable():
    """
    Ensure the required directories exist **and** are writable so the student
    can modify or create files within them.
    """
    for directory in (TICKETS_DIR, TICKET_DIR, LOGS_DIR):
        assert os.path.isdir(directory), (
            f"Required directory missing: {directory}"
        )
        assert _is_writable(directory), (
            f"Directory is not writable: {directory}"
        )


def test_app_conf_exists():
    """
    Verify that the application's configuration file is already present before
    any modification begins.
    """
    assert os.path.isfile(APP_CONF_PATH), (
        f"Configuration file not found at expected location: {APP_CONF_PATH}"
    )
    assert _is_writable(APP_CONF_PATH), (
        f"Configuration file is not writable by current user: {APP_CONF_PATH}"
    )


def test_app_conf_contains_port_8080_and_not_9090():
    """
    The initial config must show Network.port == 8080 and must not yet contain
    9090 (the value to be changed to).
    """
    parser = _read_ini_file(APP_CONF_PATH)

    # Presence of section/key
    assert parser.has_section("Network"), (
        f"[Network] section missing in {APP_CONF_PATH}"
    )
    assert parser.has_option("Network", "port"), (
        f"'port' key missing in [Network] section of {APP_CONF_PATH}"
    )

    port_value = parser.get("Network", "port").strip()
    assert port_value == "8080", (
        f"Expected 'port' to be 8080 in initial state; found '{port_value}' "
        f"in {APP_CONF_PATH}"
    )
    assert port_value != "9090", (
        "Configuration already contains port 9090; it should still be 8080 "
        "before the ticket is resolved."
    )


def test_resolution_log_does_not_exist_yet():
    """
    The resolution log should not exist prior to the student's actions.
    """
    assert not os.path.exists(RESOLUTION_LOG), (
        f"Resolution log {RESOLUTION_LOG} should NOT exist yet, but it does."
    )