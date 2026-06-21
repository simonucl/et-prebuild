# test_initial_state.py
# Pytest suite to validate the initial filesystem state **before** the student
# performs any action for ticket #425.
#
# Rules being validated (truth value):
# 1. Directory /home/user/services/app-service/ exists and contains:
#       - config.yml  (with "maintenance: true" exactly once)
#       - restart.sh  (must be executable)
# 2. File /home/user/services/app-service/restart.log does NOT exist yet.
# 3. File /home/user/ticket-425.log does NOT exist yet.

import os
import stat
import pytest
from typing import List

APP_SERVICE_DIR = "/home/user/services/app-service"
CONFIG_PATH = os.path.join(APP_SERVICE_DIR, "config.yml")
RESTART_SH_PATH = os.path.join(APP_SERVICE_DIR, "restart.sh")
RESTART_LOG_PATH = os.path.join(APP_SERVICE_DIR, "restart.log")
TICKET_LOG_PATH = "/home/user/ticket-425.log"


@pytest.fixture(scope="module")
def config_lines() -> List[str]:
    """Return the stripped lines of config.yml."""
    assert os.path.isfile(CONFIG_PATH), (
        f"Expected configuration file {CONFIG_PATH!r} to exist, "
        "but it is missing."
    )
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f]


def test_app_service_directory_exists():
    assert os.path.isdir(APP_SERVICE_DIR), (
        f"Directory {APP_SERVICE_DIR!r} is missing. "
        "The initial environment should contain the app-service directory."
    )


def test_restart_sh_exists_and_executable():
    assert os.path.isfile(RESTART_SH_PATH), (
        f"Helper script {RESTART_SH_PATH!r} is missing."
    )

    st = os.stat(RESTART_SH_PATH)
    is_executable = bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
    assert is_executable, (
        f"Helper script {RESTART_SH_PATH!r} exists but is not marked executable."
    )


def test_config_has_single_maintenance_true(config_lines):
    """
    The YAML config must contain the line 'maintenance: true' exactly once and
    must NOT contain 'maintenance: false'. This ensures the application really
    starts in maintenance mode prior to the student's actions.
    """
    maintenance_true_lines = [ln for ln in config_lines if ln.strip() == "maintenance: true"]
    maintenance_false_lines = [ln for ln in config_lines if ln.strip() == "maintenance: false"]

    assert len(maintenance_true_lines) == 1, (
        "config.yml should contain the line 'maintenance: true' exactly once "
        f"before fixes are applied. Found {len(maintenance_true_lines)} such lines."
    )

    assert len(maintenance_false_lines) == 0, (
        "config.yml already contains 'maintenance: false' before the student "
        "has a chance to edit it. Initial state must have it set to true."
    )


def test_restart_log_does_not_exist_yet():
    assert not os.path.exists(RESTART_LOG_PATH), (
        f"Restart log {RESTART_LOG_PATH!r} already exists. "
        "It should only be created after the student executes restart.sh."
    )


def test_ticket_log_does_not_exist_yet():
    assert not os.path.exists(TICKET_LOG_PATH), (
        f"Ticket note {TICKET_LOG_PATH!r} already exists. "
        "It should be created by the student when the ticket is resolved."
    )