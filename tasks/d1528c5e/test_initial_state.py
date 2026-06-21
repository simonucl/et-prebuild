# test_initial_state.py
#
# This pytest suite verifies that the *initial* filesystem state expected
# by the exercise is present **before** the student performs any action.
#
# Checked items:
#   1. Directory /home/user/db_backup/conf exists.
#   2. File     /home/user/db_backup/conf/backup.ini exists.
#   3. The INI file has exactly the two sections `primary` and `secondary`
#      and each section contains the five required keys with the expected
#      values.

from pathlib import Path
import configparser
import pytest

CONF_DIR = Path("/home/user/db_backup/conf")
INI_FILE = CONF_DIR / "backup.ini"

EXPECTED = {
    "primary": {
        "db_name": "customer_orders",
        "host": "db-primary.local",
        "port": "5432",
        "last_full_backup": "2023-06-01 00:00:00",
    },
    "secondary": {
        "db_name": "analytics",
        "host": "db-secondary.local",
        "port": "5433",
        "last_full_backup": "2023-06-01 02:00:00",
    },
}


def test_conf_directory_exists():
    """The configuration directory must already exist."""
    assert CONF_DIR.exists(), f"Missing directory: {CONF_DIR}"
    assert CONF_DIR.is_dir(), f"Path exists but is not a directory: {CONF_DIR}"


def test_backup_ini_exists():
    """The backup.ini file must already exist inside the conf directory."""
    assert INI_FILE.exists(), f"Missing file: {INI_FILE}"
    assert INI_FILE.is_file(), f"Path exists but is not a regular file: {INI_FILE}"


def test_backup_ini_content():
    """
    The INI file must contain exactly the expected sections and key/value pairs.
    Minor variations in whitespace are tolerated because we parse via configparser.
    """
    parser = configparser.ConfigParser()
    parser.optionxform = str  # preserve case of keys (though all are lowercase here)
    read_files = parser.read(INI_FILE)
    assert read_files, f"Could not read INI file at {INI_FILE}"

    # Verify sections.
    existing_sections = parser.sections()
    expected_sections = list(EXPECTED.keys())
    assert (
        existing_sections == expected_sections
    ), (
        f"INI file sections mismatch.\n"
        f"Expected sections (in order): {expected_sections}\n"
        f"Found sections           : {existing_sections}"
    )

    # Verify each key/value pair.
    for section, kv in EXPECTED.items():
        assert parser.has_section(section), f"Missing section [{section}] in {INI_FILE}"
        for key, expected_value in kv.items():
            assert parser.has_option(
                section, key
            ), f"Missing key '{key}' in section [{section}]"
            actual_value = parser.get(section, key)
            assert (
                actual_value == expected_value
            ), (
                f"Value mismatch in section [{section}] for key '{key}'.\n"
                f"Expected: {expected_value!r}\n"
                f"Found   : {actual_value!r}"
            )