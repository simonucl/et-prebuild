# test_initial_state.py
#
# This test-suite validates the **initial** state of the operating system
# _before_ the student’s solution is executed.  It confirms that the only
# pre-existing asset is the INI file that the task description guarantees.
#
# IMPORTANT:
# • Do **NOT** add tests for any output artefacts that the student is
#   supposed to create (e.g. /home/user/webapp/reports or its files).
# • Failures must clearly indicate what is missing or incorrect.
#
# Only the Python stdlib and pytest are used.

import os
import pytest

INI_PATH = "/home/user/webapp/config/settings.ini"

# Exact byte-for-byte content expected in the INI file.
# A trailing newline character is included intentionally.
EXPECTED_INI_CONTENT = (
    "[server]\n"
    "host = 0.0.0.0\n"
    "port = 8080\n"
    "\n"
    "[email]\n"
    "smtp_host = mail.example.com\n"
    "smtp_port = 587\n"
    "username = notify@example.com\n"
    "password = mailingR0cks!\n"
    "\n"
    "[database]\n"
    "host = 172.16.24.10\n"
    "port = 5432\n"
    "user = webapp\n"
    "password = s3cr3t!\n"
    "\n"
    "[feature_flags]\n"
    "dark_mode = true\n"
    "beta_payments = false\n"
)


def test_settings_ini_exists():
    """
    Verify that /home/user/webapp/config/settings.ini is present and is a file.
    """
    assert os.path.isfile(INI_PATH), (
        f"Expected file not found: {INI_PATH}\n"
        "The task requires this file to be present before any action is taken."
    )


def test_settings_ini_content_is_pristine():
    """
    Ensure the INI file matches the pristine state expected by the task
    description.  Any deviation means the starting point is incorrect.
    """
    with open(INI_PATH, "r", encoding="utf-8") as fh:
        actual_content = fh.read()

    assert actual_content == EXPECTED_INI_CONTENT, (
        "The contents of settings.ini do not match the expected initial state.\n"
        "If the file has been altered, please restore it exactly as specified "
        "in the task description."
    )