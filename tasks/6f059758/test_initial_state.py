# test_initial_state.py
#
# This pytest file verifies that the operating-system / filesystem is in the
# expected **initial** state *before* the student flips the configuration from
# “development” to “production”.  It checks that:
#
# 1. The two configuration files exist and still contain the original
#    “development” values.
# 2. The audit-log directory (/home/user/update_logs) does NOT exist yet.
#
# If any assertion fails, the error message pin-points exactly what is missing
# or wrong so that the student knows the initial state is incorrect.

from pathlib import Path
import pytest


SITE_CONFIG_PATH = Path("/home/user/project/config/site_config.yaml")
DATABASE_TOML_PATH = Path("/home/user/project/config/database.toml")
UPDATE_LOGS_DIR = Path("/home/user/update_logs")


@pytest.fixture(scope="module")
def site_config_content():
    """Return the raw text of site_config.yaml (or fail if the file is missing)."""
    assert SITE_CONFIG_PATH.is_file(), (
        f"Expected configuration file not found: {SITE_CONFIG_PATH}"
    )
    return SITE_CONFIG_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def database_toml_content():
    """Return the raw text of database.toml (or fail if the file is missing)."""
    assert DATABASE_TOML_PATH.is_file(), (
        f"Expected configuration file not found: {DATABASE_TOML_PATH}"
    )
    return DATABASE_TOML_PATH.read_text(encoding="utf-8")


def test_site_config_yaml_initial_state(site_config_content):
    """
    The YAML file must still be in *development* mode:
      production: false
      assets.css_minify: false
    """
    expected_lines = [
        'site_name: "My Portfolio"',
        "production: false",
        "assets:",
        "  js_minify: false",
        "  css_minify: false",
    ]

    actual_lines = site_config_content.rstrip("\n").splitlines()
    assert actual_lines == expected_lines, (
        f"{SITE_CONFIG_PATH} does not match the expected *initial* content.\n"
        "If you have already modified the file, please revert it so that the\n"
        "tests that check the *pre-task* state pass."
    )


def test_database_toml_initial_state(database_toml_content):
    """
    The TOML file must still reference the original connection pool size of 5.
    """
    expected_lines = [
        "[database]",
        'host = "localhost"',
        "port = 5432",
        'user = "admin"',
        'password = "admin"',
        "pool_size = 5",
    ]

    actual_lines = database_toml_content.rstrip("\n").splitlines()
    assert actual_lines == expected_lines, (
        f"{DATABASE_TOML_PATH} does not match the expected *initial* content.\n"
        "If you have already modified the file, please revert it so that the\n"
        "tests that check the *pre-task* state pass."
    )


def test_update_logs_directory_absent():
    """
    The audit-log directory must *not* exist yet.  It will be created by the
    student during the task.
    """
    assert not UPDATE_LOGS_DIR.exists(), (
        f"{UPDATE_LOGS_DIR} already exists, but it should NOT be present before "
        "the task starts.  Remove the directory (or rename it) so the initial-"
        "state tests pass."
    )