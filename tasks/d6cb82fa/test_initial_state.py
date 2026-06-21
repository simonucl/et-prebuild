# test_initial_state.py
#
# This pytest suite verifies that the filesystem is still in its *initial*,
# untouched state before the student runs any commands.  It asserts that the
# translation-sync configuration directories and files do **NOT** yet exist.
#
# If any of these resources are already present, the tests will fail with a
# clear, actionable message.

import os
from pathlib import Path

# Absolute paths that must **not** exist yet.
CONFIG_DIR = Path("/home/user/.config/translation-sync")
LOCAL_DIR  = Path("/home/user/.local/share/translation-sync")

SERVICE_CONF = CONFIG_DIR / "service.conf"
PREREQ_LOG   = LOCAL_DIR  / "prerequisites.log"


def _assert_not_exists(path: Path):
    """
    Helper that fails the test if `path` (file or directory) exists.
    Produces a detailed, user-friendly failure message.
    """
    assert not path.exists(), (
        f"{path} already exists, but the exercise expects the filesystem to be "
        "clean before you start.  Remove it (or start in a fresh environment) "
        "and run the tests again."
    )


def test_config_directory_absent():
    """The main configuration directory must not be present yet."""
    _assert_not_exists(CONFIG_DIR)


def test_local_directory_absent():
    """The data/log directory must not be present yet."""
    _assert_not_exists(LOCAL_DIR)


def test_service_conf_absent():
    """The configuration file must not exist before the student creates it."""
    _assert_not_exists(SERVICE_CONF)


def test_prerequisites_log_absent():
    """The prerequisites log must not exist before the student creates it."""
    _assert_not_exists(PREREQ_LOG)