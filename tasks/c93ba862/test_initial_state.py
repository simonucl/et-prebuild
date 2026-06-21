# test_initial_state.py
"""
Pytest suite that validates the **initial** operating-system / filesystem
state before the student performs any action for the “key-rotation” task.

The tests confirm that:
1. All prerequisite files/directories exist with the exact expected content.
2. None of the artefacts that the student is supposed to create/modify
   (new directory, reports, updated config, etc.) are present yet.

Only the Python standard library and pytest are used.
"""
import os
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants ─ expected INITIAL filesystem state
# ---------------------------------------------------------------------------

HOME = Path("/home/user")

# 1. Application log ---------------------------------------------------------
APP_LOG = HOME / "logs" / "app-2023-09-01.log"
APP_LOG_EXPECTED = (
    "2023-09-01T08:15:27Z INFO download user=asmith file=document.pdf size=15234 ip=10.0.0.8\n"
    "2023-09-01T09:01:11Z INFO rotateKey user=jdoe oldKey=abc123 ip=10.0.0.5\n"
    "2023-09-01T09:05:14Z WARN cpu usage high\n"
    "2023-09-01T10:22:47Z INFO rotateKey user=asmith oldKey=def456 ip=10.0.0.8\n"
    "2023-09-01T11:45:22Z INFO rotateKey user=bwayne oldKey=ghi789 ip=10.0.0.9\n"
    "2023-09-01T12:04:55Z INFO logout user=jdoe ip=10.0.0.5\n"
)

# 2. Security audit log ------------------------------------------------------
SEC_AUDIT_LOG = HOME / "logs" / "security_audit.log"
SEC_AUDIT_EXPECTED = "2023-09-01:Audit start\n"

# 3. Application configuration ----------------------------------------------
CONFIG_FILE = HOME / ".config" / "app" / "config.yml"
CONFIG_EXPECTED = (
    'apiEndpoint: "https://api.example.com/v1/"\n'
    'apiKey: "abc123"\n'
    "timeout: 30\n"
)

# 4. Paths that MUST **NOT** exist yet ---------------------------------------
CRED_ROTATION_DIR = HOME / "credential_rotation"
ROTATION_REPORT = CRED_ROTATION_DIR / "rotation_report_2023-09-01.log"
NEW_CREDS_FILE = CRED_ROTATION_DIR / "new_credentials.env"
# ---------------------------------------------------------------------------


# ===========================================================================
# Helper utilities
# ===========================================================================

def _read_file(path: Path) -> str:
    """Return the full contents of *path* as UTF-8 text."""
    with path.open("r", encoding="utf-8") as fh:
        return fh.read()


# ===========================================================================
# Tests for initial state
# ===========================================================================

def test_logs_directory_exists():
    logs_dir = HOME / "logs"
    assert logs_dir.is_dir(), f"Required directory missing: {logs_dir}"


def test_app_log_exists_and_is_exact():
    assert APP_LOG.is_file(), f"Missing application log: {APP_LOG}"
    content = _read_file(APP_LOG)
    assert content == APP_LOG_EXPECTED, (
        "Application log content is not exactly as expected.\n"
        f"--- expected ({len(APP_LOG_EXPECTED)} bytes)\n{APP_LOG_EXPECTED}"
        f"--- found    ({len(content)} bytes)\n{content}"
    )


def test_security_audit_initial_state():
    assert SEC_AUDIT_LOG.is_file(), f"Missing security audit log: {SEC_AUDIT_LOG}"
    content = _read_file(SEC_AUDIT_LOG)
    assert content == SEC_AUDIT_EXPECTED, (
        "security_audit.log should contain exactly one initial line ending "
        "with a newline and nothing else.\n"
        f"Expected: {repr(SEC_AUDIT_EXPECTED)}\nFound   : {repr(content)}"
    )


def test_config_file_exists_and_not_yet_rotated():
    assert CONFIG_FILE.is_file(), f"Missing configuration file: {CONFIG_FILE}"
    content = _read_file(CONFIG_FILE)
    assert content == CONFIG_EXPECTED, (
        "config.yml differs from the expected initial state.\n"
        "It should still reference the ORIGINAL apiKey \"abc123\" and must "
        "NOT yet contain the rotated key.\n"
        f"Expected content:\n{CONFIG_EXPECTED}\nFound content:\n{content}"
    )
    assert "ROTATED_KEY_2023" not in content, (
        "config.yml already contains the rotated key but it should not at "
        "this stage."
    )


def test_credential_rotation_directory_absent():
    assert not CRED_ROTATION_DIR.exists(), (
        f"Directory {CRED_ROTATION_DIR} should NOT exist before the exercise starts."
    )


def test_rotation_report_absent():
    assert not ROTATION_REPORT.exists(), (
        f"Rotation report {ROTATION_REPORT} should NOT exist before the exercise starts."
    )


def test_new_credentials_file_absent():
    assert not NEW_CREDS_FILE.exists(), (
        f"New credentials file {NEW_CREDS_FILE} should NOT exist before the exercise starts."
    )