# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state before the
# student rotates the credentials.  It must be run immediately after the
# environment is provisioned and *before* the student performs any action.

import hashlib
import os
from pathlib import Path

import pytest

HOME = Path("/home/user").resolve()
CONFIG_DIR = HOME / "app" / "config"
ROTATE_DIR = HOME / "rotate"
SECURITY_DIR = HOME / "security"

DATABASE_INI = CONFIG_DIR / "database.ini"
DATABASE_BAK = CONFIG_DIR / "database.ini.bak"
NEW_PASS_FILE = ROTATE_DIR / "new_pass.txt"
ROTATION_LOG = SECURITY_DIR / "rotation.log"


@pytest.fixture(scope="module")
def expected_database_ini_content() -> str:
    """
    The exact, byte-for-byte contents that must be present in the original
    /home/user/app/config/database.ini file *before* any rotation occurs.
    """
    return (
        "[database]\n"
        "user = appuser\n"
        "password = OldPassw0rd!\n"
        "host = 127.0.0.1\n"
        "port = 5432\n"
    )


def test_database_ini_exists_and_matches(expected_database_ini_content):
    assert DATABASE_INI.exists(), (
        f"Expected {DATABASE_INI} to exist, but it is missing."
    )

    content = DATABASE_INI.read_text(encoding="utf-8")
    assert content == expected_database_ini_content, (
        f"The contents of {DATABASE_INI} do not match the expected initial "
        f"configuration.\n\nExpected:\n{expected_database_ini_content!r}\n\n"
        f"Found:\n{content!r}"
    )


def test_new_pass_file_exists_and_has_correct_first_line():
    assert NEW_PASS_FILE.exists(), (
        f"Expected {NEW_PASS_FILE} to exist, but it is missing."
    )

    lines = NEW_PASS_FILE.read_text(encoding="utf-8").splitlines()
    assert lines, f"{NEW_PASS_FILE} appears to be empty."
    first_line = lines[0]
    assert first_line == "N3wP@ssw0rd-2024!", (
        f"The first line of {NEW_PASS_FILE} was expected to be "
        f"'N3wP@ssw0rd-2024!' (without surrounding whitespace) but found "
        f"'{first_line}'."
    )

    # Optional: ensure there is nothing except possibly a blank trailing line
    assert len(lines) in {1, 2} and (len(lines) == 1 or lines[1] == ""), (
        f"{NEW_PASS_FILE} should contain only the new password on the first "
        f"line.  Found additional unexpected content: {lines[1:]}"
    )


def test_security_directory_exists_and_is_empty():
    assert SECURITY_DIR.exists(), (
        f"Expected directory {SECURITY_DIR} to exist, but it is missing."
    )
    assert SECURITY_DIR.is_dir(), (
        f"{SECURITY_DIR} exists but is not a directory."
    )

    contents = [p.name for p in SECURITY_DIR.iterdir()]
    assert not contents, (
        f"{SECURITY_DIR} is expected to be empty at the start, but it "
        f"contains: {contents}"
    )


def test_rotation_artifacts_do_not_yet_exist():
    assert not DATABASE_BAK.exists(), (
        f"Backup file {DATABASE_BAK} should NOT exist before rotation starts."
    )
    assert not ROTATION_LOG.exists(), (
        f"Audit log {ROTATION_LOG} should NOT exist before rotation starts."
    )