# test_initial_state.py
"""
Pytest suite to validate the expected *initial* operating-system / filesystem
state that must be present **before** the student starts solving the task.

The checks cover:
    • Presence and permissions of required files/directories
    • Exact contents of configuration files
    • Absence of directories/files that must not exist yet
"""

import os
import stat
from pathlib import Path

# Absolute paths used in this task
INCIDENT_DIR = Path("/home/user/incident")
BACKUP_SH = INCIDENT_DIR / "backup.sh"
ENV_FILE = INCIDENT_DIR / ".env"
ACCESS_LOG = INCIDENT_DIR / "access.log"
ENV_SECURE = INCIDENT_DIR / ".env.secure"

FIREWALL_DIR = Path("/home/user/firewall")
INCIDENT_LOGS_DIR = Path("/home/user/incident_logs")


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def file_mode(path: Path) -> int:
    """
    Return Unix permission bits for a given path as an octal integer, e.g. 0o644.
    """
    return stat.S_IMODE(path.stat().st_mode)


def assert_mode(path: Path, expected_octal: int) -> None:
    """
    Assert that path has the expected permission mode.
    """
    mode = file_mode(path)
    assert (
        mode == expected_octal
    ), f"{path} permissions are {oct(mode)}, expected {oct(expected_octal)}"


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_incident_directory_exists_and_permissions():
    assert INCIDENT_DIR.is_dir(), f"Required directory {INCIDENT_DIR} is missing"
    assert_mode(INCIDENT_DIR, 0o755)


def test_backup_sh_exists_and_is_world_writable():
    assert BACKUP_SH.is_file(), f"Required file {BACKUP_SH} is missing"
    # 0777 decimal is 0o777
    assert_mode(
        BACKUP_SH, 0o777
    ), f"{BACKUP_SH} must start as mode 0777 for the student to fix"


def test_env_file_content_and_permissions():
    assert ENV_FILE.is_file(), f"Required file {ENV_FILE} is missing"
    assert_mode(
        ENV_FILE, 0o644
    ), f"{ENV_FILE} must start with mode 0644 for the student to change later"

    # Validate exact contents
    content_lines = ENV_FILE.read_text().splitlines()
    expected_lines = [
        "SECRET_KEY=INSECURE_DEFAULT",
        "DB_PASSWORD=supersecret",
    ]
    assert (
        content_lines == expected_lines
    ), (
        f"{ENV_FILE} must contain exactly two lines:\n"
        "1) SECRET_KEY=INSECURE_DEFAULT\n"
        "2) DB_PASSWORD=supersecret\n"
        f"Found: {content_lines}"
    )


def test_access_log_exists_and_contains_offending_ip():
    assert ACCESS_LOG.is_file(), f"Required file {ACCESS_LOG} is missing"
    assert_mode(
        ACCESS_LOG, 0o644
    ), f"{ACCESS_LOG} must start with mode 0644 (readable log file)"

    log_text = ACCESS_LOG.read_text(errors="ignore")
    offending_ip = "203.0.113.50"
    assert (
        offending_ip in log_text
    ), f"{ACCESS_LOG} must already contain at least one occurrence of {offending_ip}"


def test_env_secure_does_not_exist_yet():
    assert (
        not ENV_SECURE.exists()
    ), f"{ENV_SECURE} should NOT exist before the student creates it"


def test_firewall_directory_absent():
    assert (
        not FIREWALL_DIR.exists()
    ), f"{FIREWALL_DIR} must NOT exist yet; student should create it during fix"


def test_incident_logs_directory_absent():
    assert (
        not INCIDENT_LOGS_DIR.exists()
    ), f"{INCIDENT_LOGS_DIR} must NOT exist yet; student should create it during fix"