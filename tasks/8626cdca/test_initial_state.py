# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state that must be
# present **before** you begin the credential-rotation task.  If any of these
# tests fail, do **NOT** start the rotation yet—first restore the expected
# baseline described in the assignment.

import os
from pathlib import Path


APP_DIR = Path("/home/user/app")
ENV_FILE = APP_DIR / ".env"
ENV_BACKUP = APP_DIR / ".env.bak"
ROTATION_LOG_DIR = Path("/home/user/rotation_logs")
ROTATION_LOG_FILE = ROTATION_LOG_DIR / "credential_rotation.log"


def test_app_directory_exists():
    assert APP_DIR.is_dir(), (
        f"Required directory {APP_DIR} is missing. "
        "Create it (or restore it) before running the rotation procedure."
    )


def test_env_file_exists_and_content():
    assert ENV_FILE.is_file(), (
        f"Required file {ENV_FILE} is missing. "
        "The rotation procedure starts from an existing .env file."
    )

    data = ENV_FILE.read_bytes()

    # 1. Must end with a single Unix LF (`\n`).
    assert data.endswith(b"\n"), (
        f"{ENV_FILE} must end with exactly one Unix newline (LF)."
    )

    # 2. Must NOT contain Windows CRLF endings.
    assert b"\r" not in data, (
        f"{ENV_FILE} must use Unix LF line endings, not Windows CRLF."
    )

    text = data.decode()
    lines = text.split("\n")[:-1]  # strip the final empty element after trailing LF
    expected_lines = [
        "APP_DB_USER=olduser",
        "APP_DB_PASS=oldpass123",
    ]
    assert lines == expected_lines, (
        f"{ENV_FILE} must contain exactly the two lines below, nothing more:"
        f"\n{expected_lines}\nFound:\n{lines}"
    )


def test_env_backup_not_present():
    assert not ENV_BACKUP.exists(), (
        f"Backup file {ENV_BACKUP} already exists. "
        "The backup should be created *during* the rotation process, "
        "so it must not be present beforehand."
    )


def test_rotation_log_not_present():
    assert not ROTATION_LOG_FILE.exists(), (
        f"Audit log {ROTATION_LOG_FILE} already exists. "
        "It should be generated only after the rotation completes."
    )