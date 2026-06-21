# test_initial_state.py
#
# Pytest suite that validates the *initial* filesystem state
# before the student begins the configuration-update task.
#
# It checks that:
#   1. /home/user/service_cfg/ exists.
#   2. /home/user/service_cfg/service.conf exists and has the
#      expected “pre-task” contents.
#   3. No backup or log artifacts are present yet.
#
# If any assertion fails, the error message explains exactly
# what is missing or unexpected.

from pathlib import Path
import pytest

# --- Paths used throughout the tests ---------------------------------------

BASE_DIR = Path("/home/user/service_cfg")
CONF_FILE = BASE_DIR / "service.conf"
BACKUP_FILE = BASE_DIR / "service.conf.bak"
LOGS_DIR = BASE_DIR / "logs"
DEPLOY_LOG = LOGS_DIR / "deploy.log"

# ---------------------------------------------------------------------------


def test_service_cfg_directory_exists():
    assert BASE_DIR.exists(), f"Directory {BASE_DIR} is missing."
    assert BASE_DIR.is_dir(), f"{BASE_DIR} exists but is not a directory."


def test_service_conf_exists_and_has_expected_contents():
    # 1. File presence
    assert CONF_FILE.exists(), f"Configuration file {CONF_FILE} is missing."
    assert CONF_FILE.is_file(), f"{CONF_FILE} exists but is not a file."

    # 2. File contents
    expected_lines = [
        "# Application Service Configuration",
        "version=1.8",
        "enable_new_ui=no",
    ]

    contents = CONF_FILE.read_text(encoding="utf-8")
    actual_lines = contents.rstrip("\n").split("\n")

    assert actual_lines == expected_lines, (
        f"{CONF_FILE} contents do not match the expected *initial* configuration.\n"
        f"Expected lines:\n{expected_lines}\n"
        f"Actual lines:\n{actual_lines}"
    )


def test_no_backup_or_logs_exist_yet():
    # Backup must NOT exist before the student runs their solution.
    assert not BACKUP_FILE.exists(), (
        f"Backup file {BACKUP_FILE} should NOT exist before the task is performed."
    )

    # logs/ directory should NOT exist yet.
    assert not LOGS_DIR.exists(), (
        f"Logs directory {LOGS_DIR} should NOT exist before the task is performed."
    )

    # The deploy log should certainly not exist.
    assert not DEPLOY_LOG.exists(), (
        f"Deployment log {DEPLOY_LOG} should NOT exist before the task is performed."
    )