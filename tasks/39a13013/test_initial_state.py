# test_initial_state.py
"""
Pytest suite to validate the *initial* filesystem / OS state **before** the
student performs any credential-rotation steps.

This file checks that:
1. /home/user/app/config/credentials.ini is present with the exact expected
   starting contents.
2. No backup file or audit log is present yet.

If any check fails, the student starts from an unexpected state and the test
explains what is missing or out of place.
"""
from pathlib import Path

import pytest

# -----------------------------------------------------------------------------
# Constants describing the required initial state
# -----------------------------------------------------------------------------
CONFIG_DIR = Path("/home/user/app/config")
CONFIG_FILE = CONFIG_DIR / "credentials.ini"
BACKUP_FILE = CONFIG_DIR / "credentials.ini.bak"
AUDIT_LOG = Path("/home/user/rotation.log")

EXPECTED_CONTENT_LINES = [
    "[default]",
    "access_key = AKIAEXAMPLE123456",
    "secret_key = OLDSECRET_987654321==",
    "version = 7",
]
EXPECTED_CONTENT = "\n".join(EXPECTED_CONTENT_LINES) + "\n"


# -----------------------------------------------------------------------------
# Helper(s)
# -----------------------------------------------------------------------------
def read_text(p: Path) -> str:
    """Read text from *p* assuming UTF-8; provide a useful error if it fails."""
    try:
        return p.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Unable to read {p}: {exc}")


# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------
def test_config_directory_exists():
    assert CONFIG_DIR.is_dir(), (
        f"Expected configuration directory {CONFIG_DIR} to exist "
        "before beginning the exercise."
    )


def test_credentials_ini_exists_with_expected_content():
    assert CONFIG_FILE.is_file(), (
        f"Expected {CONFIG_FILE} to exist before any changes are made."
    )

    actual = read_text(CONFIG_FILE)

    # First, check that the file matches the expected content exactly,
    # including ordering and spacing.
    if actual != EXPECTED_CONTENT:
        diff_hint = (
            "The initial credentials.ini content does not match the expected "
            "starting point.\n\n"
            "EXPECTED:\n"
            "---------\n"
            f"{EXPECTED_CONTENT}\n"
            "FOUND:\n"
            "------\n"
            f"{actual}"
        )
        pytest.fail(diff_hint)

    # Additional sanity: ensure the version is an int and the secret_key is
    # indeed the old one.
    lines = [ln.strip() for ln in actual.splitlines() if ln.strip()]
    kv = dict(line.split(" =", 1) for line in lines[1:])  # skip header
    assert kv["secret_key"].strip() == "OLDSECRET_987654321==", (
        "secret_key in the initial file must be 'OLDSECRET_987654321==' "
        "so that the student can rotate it."
    )
    assert kv["version"].strip() == "7", (
        "version in the initial file must be '7' so that the student can "
        "increment it."
    )


def test_no_backup_or_audit_log_exist_yet():
    assert not BACKUP_FILE.exists(), (
        f"Backup file {BACKUP_FILE} should NOT exist yet; "
        "it will be created by the student."
    )
    assert not AUDIT_LOG.exists(), (
        f"Audit log {AUDIT_LOG} should NOT exist yet; "
        "it will be created by the student."
    )