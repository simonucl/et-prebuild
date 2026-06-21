# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state **before**
# the student performs any actions for the “inventory-service” migration
# exercise.  It intentionally checks only pre-existing resources and
# avoids asserting on any files or directories that the student is
# expected to create (e.g., /home/user/migration_logs/).

import pathlib
import pytest

# ----------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------

SERVICE_DIR = pathlib.Path("/home/user/microservices/inventory-service")
CONFIG_PATH = SERVICE_DIR / "config.json"

OLD_DBHOST_SUBSTRING = '"dbHost": "db.internal.old-cluster.local"'
NEW_DBHOST_SUBSTRING = '"dbHost": "db.internal.new-cluster.local"'


# ----------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------

def test_service_directory_exists():
    """Ensure the microservice directory is present."""
    assert SERVICE_DIR.exists(), (
        f"Expected directory {SERVICE_DIR} to exist, but it is missing."
    )
    assert SERVICE_DIR.is_dir(), (
        f"Expected {SERVICE_DIR} to be a directory, but it is not."
    )


def test_config_file_exists():
    """Ensure the configuration file exists and is a regular file."""
    assert CONFIG_PATH.exists(), (
        f"Expected configuration file {CONFIG_PATH} to exist, but it is missing."
    )
    assert CONFIG_PATH.is_file(), (
        f"Expected {CONFIG_PATH} to be a regular file, but it is not."
    )


def test_config_contains_old_dbhost_and_not_new():
    """
    The config.json must reference the *old* database host and *not* the new one.
    """
    try:
        content = CONFIG_PATH.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Could not read {CONFIG_PATH}: {exc}")

    assert OLD_DBHOST_SUBSTRING in content, (
        f"The file {CONFIG_PATH} does not contain the expected line:\n"
        f"    {OLD_DBHOST_SUBSTRING}\n"
        "Make sure the starting state includes the old dbHost value."
    )

    assert NEW_DBHOST_SUBSTRING not in content, (
        f"The file {CONFIG_PATH} already contains the new dbHost value:\n"
        f"    {NEW_DBHOST_SUBSTRING}\n"
        "The initial state should still point to the *old* cluster."
    )