# test_initial_state.py
# Pytest suite that verifies the OS / filesystem **before** the student performs
# any credential-rotation actions for the given task.
#
# The expected initial situation is:
#   • /home/user/app/config/settings.ini   exists with the ORIGINAL (old) secrets.
#   • /home/user/rotation_logs/rotation_20230918_120000.log  does NOT exist yet.
#
# These tests must pass *before* the student starts working.  If they fail,
# the exercise environment is in an unexpected state.

from pathlib import Path
import pytest


# ---------------------------------------------------------------------------
# Constants describing the correct, pristine state *before* the rotation.
# ---------------------------------------------------------------------------

SETTINGS_INI_PATH = Path("/home/user/app/config/settings.ini")
ROTATION_LOG_PATH = Path("/home/user/rotation_logs/rotation_20230918_120000.log")

EXPECTED_SETTINGS_CONTENT = (
    "[database]\n"
    "user = app_user\n"
    "password = oldDBpwd123\n"
    "\n"
    "[api]\n"
    "key = OLDAPIKEY0987654321\n"
    "\n"
    "[general]\n"
    "debug = false\n"
)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_settings_ini_exists_and_is_pristine():
    """
    The settings.ini file must exist and contain the *original* secrets.
    """
    assert SETTINGS_INI_PATH.exists(), (
        f"Required file {SETTINGS_INI_PATH} is missing. "
        "The exercise must start with this file present."
    )
    assert SETTINGS_INI_PATH.is_file(), (
        f"{SETTINGS_INI_PATH} exists but is not a regular file."
    )

    actual_content = SETTINGS_INI_PATH.read_text()

    # 1. Exact byte-for-byte match (including trailing LF at end of file).
    assert actual_content == EXPECTED_SETTINGS_CONTENT, (
        f"{SETTINGS_INI_PATH} content is not the expected initial version.\n"
        "Expected:\n"
        "----------------------------------------\n"
        f"{EXPECTED_SETTINGS_CONTENT}\n"
        "----------------------------------------\n"
        "Found:\n"
        "----------------------------------------\n"
        f"{actual_content}\n"
        "----------------------------------------"
    )

    # 2. Sanity check: the NEW secrets must *not* yet be present.
    forbidden_strings = ["S3cureDBp@55w0rd!", "A1b2C3d4E5F6G7H8"]
    for secret in forbidden_strings:
        assert secret not in actual_content, (
            f"Secret value {secret!r} already present in {SETTINGS_INI_PATH}. "
            "Rotation appears to have been done prematurely."
        )


def test_rotation_log_not_present_yet():
    """
    The rotation log file must *not* exist before any action is taken.
    The containing directory may or may not exist—only the file's absence
    is enforced here.
    """
    assert not ROTATION_LOG_PATH.exists(), (
        f"Rotation log {ROTATION_LOG_PATH} already exists. "
        "The environment should start without this file so the student can create it."
    )