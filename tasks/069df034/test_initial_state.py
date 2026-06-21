# test_initial_state.py
#
# Pytest suite that validates the starting filesystem state for the
# “credential-rotation” exercise _before_ the student makes any changes.
#
# It checks that:
#   • /home/user/app_configs/ exists and contains exactly four *.ini files.
#   • Each of the four files exists with the precise, expected contents.
#   • No backups directory exists yet.
#   • No rotation-logs directory (and therefore no log file) exists yet.
#
# The tests use only the Python standard library and pytest.


import os
from pathlib import Path

import pytest


# ----- constants -----------------------------------------------------------------

APPCONFIG_DIR = Path("/home/user/app_configs")
INI_FILES = {
    "webapp.ini": (
        "[general]\n"
        "port=8080\n"
        "\n"
        "[credentials]\n"
        "username=web_admin\n"
        "password=OldWebPass123!\n"
    ),
    "dbservice.ini": (
        "[service]\n"
        "host=127.0.0.1\n"
        "\n"
        "[credentials]\n"
        "username=db_root\n"
        "password=OldDbPass456!\n"
    ),
    "mqbroker.ini": (
        "[broker]\n"
        "queues=8\n"
        "\n"
        "[credentials]\n"
        "username=mq_manager\n"
        "password=OldMqPass789!\n"
    ),
    "analytics.ini": (
        "[analytics]\n"
        "enabled=true\n"
        "\n"
        "[credentials]\n"
        "username=analyst\n"
        "password=OldAnalystPass000!\n"
    ),
}

BACKUPS_DIR = APPCONFIG_DIR / "backups"
ROTATION_LOG_DIR = Path("/home/user/rotation_logs")
ROTATION_LOG_FILE = ROTATION_LOG_DIR / "credentials_rotation.log"


# ----- helper --------------------------------------------------------------------

def _read_file(path: Path) -> str:
    """Return the entire file contents as text (UTF-8)."""
    return path.read_text(encoding="utf-8")


# ----- tests ---------------------------------------------------------------------


def test_appconfig_directory_exists_and_is_directory():
    assert APPCONFIG_DIR.exists(), f"Required directory {APPCONFIG_DIR} does not exist."
    assert APPCONFIG_DIR.is_dir(), f"{APPCONFIG_DIR} exists but is not a directory."


def test_exactly_four_ini_files_present():
    found_ini_files = sorted(f.name for f in APPCONFIG_DIR.iterdir() if f.is_file() and f.suffix == ".ini")
    expected_files = sorted(INI_FILES.keys())
    assert found_ini_files == expected_files, (
        "The /home/user/app_configs directory must contain exactly the four expected "
        f"INI files.\nExpected: {expected_files}\nFound   : {found_ini_files}"
    )


@pytest.mark.parametrize("filename,expected_content", INI_FILES.items())
def test_each_ini_file_has_expected_content(filename, expected_content):
    file_path = APPCONFIG_DIR / filename
    assert file_path.exists(), f"Missing required file: {file_path}"
    actual_content = _read_file(file_path)
    assert actual_content == expected_content, (
        f"File {file_path} does not match the expected initial contents.\n"
        "---- expected ----\n"
        f"{expected_content}\n"
        "---- actual ------\n"
        f"{actual_content}"
    )


def test_backups_directory_does_not_exist_yet():
    assert not BACKUPS_DIR.exists(), (
        f"The backups directory {BACKUPS_DIR} should NOT exist before the credential-rotation task starts."
    )


def test_rotation_logs_directory_and_file_do_not_exist_yet():
    assert not ROTATION_LOG_DIR.exists(), (
        f"The rotation-logs directory {ROTATION_LOG_DIR} should NOT exist before the task starts."
    )
    assert not ROTATION_LOG_FILE.exists(), (
        f"The rotation log file {ROTATION_LOG_FILE} should NOT be present before the task starts."
    )