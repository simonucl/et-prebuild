# test_initial_state.py
#
# This test-suite validates the *initial* state of the filesystem
# before the student performs any action.  It asserts that:
#
# 1. /home/user/db exists with mode 0755.
# 2. /home/user/db/postgresql.conf exists and contains the expected
#    default contents (with work_mem set to 4MB).
# 3. /home/user/logs exists with mode 0755 and is completely empty.
#
# Only Python's standard library and pytest are used.

import os
import stat
import pytest

HOME = "/home/user"
DB_DIR = os.path.join(HOME, "db")
CONF_FILE = os.path.join(DB_DIR, "postgresql.conf")
LOGS_DIR = os.path.join(HOME, "logs")

EXPECTED_CONF_CONTENT = (
    "# PostgreSQL configuration file\n"
    "# Memory settings\n"
    "work_mem = 4MB\n"
    "# End\n"
)


def _mode(path):
    """Return the permission bits (e.g. 0o755) of *path*."""
    return stat.S_IMODE(os.lstat(path).st_mode)


def test_db_directory_exists_and_permissions():
    assert os.path.isdir(DB_DIR), (
        f"Required directory {DB_DIR} is missing."
    )
    assert _mode(DB_DIR) == 0o755, (
        f"{DB_DIR} must have permissions 755 "
        f"(found {oct(_mode(DB_DIR))})."
    )


def test_postgresql_conf_initial_content():
    assert os.path.isfile(CONF_FILE), (
        f"Required file {CONF_FILE} is missing."
    )

    with open(CONF_FILE, "r", encoding="utf-8") as fh:
        content = fh.read()

    # Normalise trailing newline: having *one* at EOF is fine, but
    # anything else (missing or extra content) is not.
    if content and not content.endswith("\n"):
        pytest.fail(
            f"{CONF_FILE} is expected to end with a newline."
        )

    assert content == EXPECTED_CONF_CONTENT, (
        f"{CONF_FILE} does not contain the expected default "
        f"configuration.\n\nExpected:\n{EXPECTED_CONF_CONTENT!r}\n\n"
        f"Found:\n{content!r}"
    )


def test_logs_directory_empty_and_permissions():
    assert os.path.isdir(LOGS_DIR), (
        f"Required directory {LOGS_DIR} is missing."
    )
    assert _mode(LOGS_DIR) == 0o755, (
        f"{LOGS_DIR} must have permissions 755 "
        f"(found {oct(_mode(LOGS_DIR))})."
    )

    contents = os.listdir(LOGS_DIR)
    assert contents == [], (
        f"{LOGS_DIR} must be empty at the start, but it contains: "
        f"{', '.join(contents) or '(nothing)'}"
    )