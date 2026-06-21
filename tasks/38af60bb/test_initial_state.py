# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state **before** the
# student begins work on the “INI audit-log” assignment.  It asserts that:
#
# 1. The pre-existing configuration file /home/user/compliance/app.conf
#    • exists
#    • has permissions 0644 (rw-r--r--)
#    • contains the exact expected key/value pairs
#
# 2. The target output artefacts do *not* yet exist:
#       /home/user/compliance/audit/          ← directory must not pre-exist
#       /home/user/compliance/audit/audit.log ← file must not pre-exist
#
# Any deviation from the expected pristine state will raise a clear, actionable
# pytest failure so that the learner starts from a clean, known-good baseline.
#
# NOTE: Only Python stdlib and pytest are used, per project constraints.

import os
import stat
import configparser
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

CONF_PATH = Path("/home/user/compliance/app.conf")
AUDIT_DIR = Path("/home/user/compliance/audit")
AUDIT_FILE = AUDIT_DIR / "audit.log"

EXPECTED_PERMS_FILE_644 = 0o644
EXPECTED_SETTINGS = {
    ("Security", "encryption"): "AES256",
    ("Security", "password_policy"): "strong",
    ("Network", "port"): "443",
    ("Network", "tls"): "enabled",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _mode(path: Path) -> int:
    """
    Return filesystem mode bits for *path* (i.e., 0o644).
    """
    return stat.S_IMODE(path.stat().st_mode)


def _read_config(path: Path) -> configparser.ConfigParser:
    """
    Parse an INI file using configparser with case-sensitive keys and section
    names preserved exactly as written.
    """
    parser = configparser.ConfigParser()
    parser.optionxform = str  # preserve case of option names
    with path.open() as fp:
        parser.read_file(fp)
    return parser


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_app_conf_exists_and_permissions():
    assert CONF_PATH.exists(), (
        f"Required configuration file not found: {CONF_PATH}"
    )
    assert CONF_PATH.is_file(), f"{CONF_PATH} exists but is not a regular file"
    perms = _mode(CONF_PATH)
    assert perms == EXPECTED_PERMS_FILE_644, (
        f"{CONF_PATH} permissions are {oct(perms)}, expected 0o644"
    )


def test_app_conf_contains_expected_settings():
    parser = _read_config(CONF_PATH)

    missing_pairs = []
    mismatched_pairs = []

    for (section, key), expected_val in EXPECTED_SETTINGS.items():
        if not parser.has_section(section):
            missing_pairs.append(f"missing section [{section}]")
            continue
        if not parser.has_option(section, key):
            missing_pairs.append(f"missing key '{key}' in section [{section}]")
            continue

        actual_val = parser.get(section, key).strip()
        if actual_val != expected_val:
            mismatched_pairs.append(
                f"[{section}] {key}={actual_val!r} (expected {expected_val!r})"
            )

    if missing_pairs or mismatched_pairs:
        lines = []
        if missing_pairs:
            lines.append(
                "Missing sections / keys:\n  - " + "\n  - ".join(missing_pairs)
            )
        if mismatched_pairs:
            lines.append(
                "Value mismatches:\n  - " + "\n  - ".join(mismatched_pairs)
            )
        pytest.fail("\n".join(lines))


def test_audit_directory_does_not_exist_yet():
    """
    The audit output directory should not pre-exist before the student runs
    their solution.  Its presence would indicate leftover artefacts from a
    previous run or an incorrectly-provisioned environment.
    """
    assert not AUDIT_DIR.exists(), (
        f"Unexpected directory present before task execution: {AUDIT_DIR}"
    )


def test_audit_log_file_does_not_exist_yet():
    """
    Likewise, the audit.log file must not be present at the start.
    """
    assert not AUDIT_FILE.exists(), (
        f"Unexpected file present before task execution: {AUDIT_FILE}"
    )