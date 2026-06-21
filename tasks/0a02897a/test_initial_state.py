# test_initial_state.py
#
# This pytest file validates the *initial* state of the operating system
# before the student performs any actions for the backup-web-server task.
#
# ────────────────────────────────────────────────────────────────────────────
# What is checked (and WHY):
#
# 1. /home/user/db_backups  …must already exist: it is the source directory
#    for the SQL dump that the student will later expose.
#
# 2. /home/user/db_backups/backup_2023_09_01.sql  …must already exist and
#    contain exactly the expected text (`SELECT 1;\n`).  This guarantees that
#    the input file is present and uncorrupted before the student begins.
#
# NOTE:  Per the grading-suite rules we intentionally do *NOT* test for the
#        presence or absence of any *output* files, directories, or processes
#        (e.g. /home/user/public_backups, backup_server.log, port 9090, …).
#
# Only stdlib + pytest are used.

from pathlib import Path
import pytest

DB_BACKUP_DIR = Path("/home/user/db_backups")
BACKUP_FILE = DB_BACKUP_DIR / "backup_2023_09_01.sql"
EXPECTED_CONTENT = "SELECT 1;\n"


def test_db_backup_directory_exists():
    """
    The source directory /home/user/db_backups must already be in place.
    """
    assert DB_BACKUP_DIR.is_dir(), (
        f"Expected directory {DB_BACKUP_DIR} to exist, "
        "but it is missing. The initial database backup directory is required "
        "for the exercise."
    )


def test_backup_sql_file_exists():
    """
    The SQL dump file must already exist inside the source directory.
    """
    assert BACKUP_FILE.is_file(), (
        f"Expected file {BACKUP_FILE} to exist, "
        "but it is missing. This file is the input that the student will "
        "copy to the public web root."
    )


def test_backup_sql_file_contents():
    """
    The SQL dump must contain the exact expected contents so that later
    byte-for-byte comparisons during grading are meaningful.
    """
    file_bytes = BACKUP_FILE.read_bytes()
    try:
        text = file_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        pytest.fail(
            f"{BACKUP_FILE} is not valid UTF-8 or is corrupt: {exc}"
        )

    assert text == EXPECTED_CONTENT, (
        f"{BACKUP_FILE} does not contain the expected text.\n"
        f"Expected (repr): {EXPECTED_CONTENT!r}\n"
        f"Found    (repr): {text!r}"
    )