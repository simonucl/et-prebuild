# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the filesystem for the
# “Bring MegaCRM back online” exercise **before** the student performs any
# actions.  These tests intentionally confirm that the legacy / “old” files
# are still present and unchanged, and that no artefacts from the *expected
# final state* are visible yet.

from pathlib import Path
import pytest

HOME = Path("/home/user")
APP_DIR = HOME / "app"
CONFIG_DIR = APP_DIR / "config"
CERTS_DIR = APP_DIR / "certs"
LOGS_DIR = APP_DIR / "logs"

SETTINGS_YML = CONFIG_DIR / "settings.yml"
DATABASE_TOML = CONFIG_DIR / "database.toml"
CHANGE_LOG = LOGS_DIR / "config_change.log"


@pytest.fixture(autouse=True)
def _assert_base_directories_exist():
    """
    Sanity-check that the top-level application directory structure exists.
    """
    for path in [APP_DIR, CONFIG_DIR]:
        assert path.is_dir(), (
            f"Expected directory {path} to exist before any student action."
        )


def test_settings_yaml_is_old_version():
    """
    /home/user/app/config/settings.yml should still contain the legacy content:
      * version == "2.3.0"
      * maintenance_mode == false
      * max_connections == 80
    It must NOT yet contain any of the new keys or values that belong to the
    *target* content (e.g., cache: section, version 2.3.1, maintenance_mode=true).
    """
    assert SETTINGS_YML.is_file(), (
        f"The file {SETTINGS_YML} is missing; it must be present before the task starts."
    )

    text = SETTINGS_YML.read_text().splitlines()

    # Positive checks (must be present)
    required_lines = {
        '  version: "2.3.0"',
        "maintenance_mode: false",
        "  max_connections: 80",
    }
    for line in required_lines:
        assert line in text, (
            f"{SETTINGS_YML} should still contain the line:\n{line!r}\n"
            "This indicates the student has not yet updated the file."
        )

    # Negative checks (must NOT be present yet)
    forbidden_fragments = [
        '  version: "2.3.1"',
        "maintenance_mode: true",
        "cache:",
    ]
    for fragment in forbidden_fragments:
        assert all(fragment not in l for l in text), (
            f"{SETTINGS_YML} already contains {fragment!r}, "
            "but this should only appear *after* the student edits the file."
        )


def test_database_toml_is_old_version():
    """
    /home/user/app/config/database.toml should still contain only the legacy
    [database] section pointing at localhost with the old credentials.
    It must NOT yet include timeout_seconds, connection_pool, tls, or the new
    host/user/password values.
    """
    assert DATABASE_TOML.is_file(), (
        f"The file {DATABASE_TOML} is missing; it must be present before the task starts."
    )

    text = DATABASE_TOML.read_text().splitlines()

    # Positive checks (must be present)
    required_lines = {
        'host = "localhost"',
        'user = "legacy_user"',
        'password = "changeme"',
    }
    for line in required_lines:
        assert line in text, (
            f"{DATABASE_TOML} should still contain the line:\n{line!r}\n"
            "This indicates the student has not yet updated the file."
        )

    # Negative checks (must NOT be present yet)
    forbidden_fragments = [
        "timeout_seconds",
        "[database.connection_pool]",
        "[database.tls]",
        'host = "db.megacrm.internal"',
        'user = "crm_app"',
        'password = "s3cr3t"',
    ]
    for fragment in forbidden_fragments:
        assert all(fragment not in l for l in text), (
            f"{DATABASE_TOML} already contains {fragment!r}, "
            "but this should only appear *after* the student edits the file."
        )


def test_cert_stub_exists():
    """
    The stub certificate file should already be in place.
    """
    cert_file = CERTS_DIR / "db-client.pem"
    assert cert_file.is_file(), (
        f"Expected stub certificate {cert_file} to exist before any changes."
    )


def test_change_log_not_present_yet():
    """
    /home/user/app/logs/config_change.log should NOT exist before the student
    performs the required edits.  The logs directory itself may or may not
    pre-exist, and that is acceptable either way.
    """
    # If the logs directory is already present, ensure the change log is absent.
    if LOGS_DIR.exists():
        assert LOGS_DIR.is_dir(), f"{LOGS_DIR} exists but is not a directory."
        assert not CHANGE_LOG.exists(), (
            f"{CHANGE_LOG} should not exist yet; it must be created by the student."
        )