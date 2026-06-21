# test_initial_state.py
#
# This pytest suite validates the *initial* state of the operating system /
# filesystem **before** the student performs any actions for the “backup
# scheduler” task.  It asserts that the configuration file hierarchy is
# present as described and that the logs directory has NOT yet been created.
#
# If any of these assertions fail, the test output will explain exactly what
# is missing or out‐of‐place.

import os
import stat
import configparser
import pytest

HOME = "/home/user"
CONF_DIR = os.path.join(HOME, "backups", "conf")
CONF_FILE = os.path.join(CONF_DIR, "db_backup.ini")
LOGS_DIR = os.path.join(HOME, "backups", "logs")

EXPECTED_INI_CONTENT = (
    "[schedule]\n"
    "daily_time = 02:30\n"
    "weekly_day = Sun\n"
    "weekly_time = 03:00\n"
)

@pytest.fixture(scope="module")
def conf_stat():
    """Return os.stat_result for /home/user/backups/conf."""
    return os.stat(CONF_DIR)

def test_conf_directory_exists_and_mode(conf_stat):
    # Presence
    assert stat.S_ISDIR(conf_stat.st_mode), (
        f"Expected {CONF_DIR!r} to exist and be a directory, "
        "but it is missing or not a directory."
    )

    # Permissions (mode 755 only)
    mode = conf_stat.st_mode & 0o777
    expected_mode = 0o755
    assert mode == expected_mode, (
        f"Directory {CONF_DIR!r} should have permissions 0o755; "
        f"found 0o{mode:o} instead."
    )

def test_config_file_exists_and_content():
    assert os.path.isfile(CONF_FILE), (
        f"Expected configuration file {CONF_FILE!r} to exist, "
        "but it is missing."
    )

    with open(CONF_FILE, "r", encoding="utf-8") as fh:
        data = fh.read()

    assert data == EXPECTED_INI_CONTENT, (
        "Configuration file content mismatch.\n"
        "---- Expected ----\n"
        f"{EXPECTED_INI_CONTENT!r}\n"
        "---- Found ----\n"
        f"{data!r}"
    )

def test_ini_parses_and_weekly_time_is_correct():
    """Extra guard: the INI parses and weekly_time is 03:00."""
    parser = configparser.ConfigParser()
    parser.read(CONF_FILE, encoding="utf-8")

    assert parser.has_section("schedule"), (
        "INI file missing [schedule] section."
    )
    weekly_time = parser.get("schedule", "weekly_time", fallback=None)
    assert weekly_time == "03:00", (
        f"[schedule].weekly_time should be '03:00', found {weekly_time!r}"
    )

def test_logs_directory_does_not_exist_yet():
    assert not os.path.exists(LOGS_DIR), (
        f"Directory {LOGS_DIR!r} must NOT exist in the initial state, "
        "but it is already present."
    )