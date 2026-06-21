# test_initial_state.py
#
# This test-suite validates the system **before** the student carries out any
# actions.  It deliberately *fails* if pre-existing artefacts from the final
# state are already present or if the given SQLite database is not in the
# expected shape.

import os
import stat
import sqlite3
import pytest
from pathlib import Path

HOME = Path("/home/user")
DB_DIR = HOME / "databases"
DB_FILE = DB_DIR / "warehouse.db"

BACKUP_DIR = HOME / "backups"
BACKUP_SQL = BACKUP_DIR / "warehouse_backup.sql"
BACKUP_GZ  = BACKUP_DIR / "warehouse_backup.sql.gz"
BACKUP_SHA = BACKUP_DIR / "warehouse_backup.sha256"
BACKUP_LOG = BACKUP_DIR / "backup_log.txt"

##############################
# 1. Checks on /home/user/databases
##############################

def test_databases_directory_exists_and_has_correct_permissions():
    assert DB_DIR.exists(), f"Required directory {DB_DIR} is missing."
    assert DB_DIR.is_dir(), f"{DB_DIR} exists but is not a directory."

    mode = DB_DIR.stat().st_mode
    perms = stat.S_IMODE(mode)
    expected = 0o755
    assert perms == expected, (
        f"Directory {DB_DIR} must have permissions {oct(expected)}, "
        f"but has {oct(perms)}."
    )

def test_warehouse_db_file_exists_and_is_valid_sqlite():
    assert DB_FILE.exists(), f"SQLite file {DB_FILE} is missing."
    assert DB_FILE.is_file(), f"{DB_FILE} exists but is not a regular file."

    # Attempt to open the database to ensure it is a valid SQLite file.
    try:
        with sqlite3.connect(str(DB_FILE)) as conn:
            conn.execute("PRAGMA schema_version;")
    except sqlite3.DatabaseError as exc:
        pytest.fail(f"{DB_FILE} is not a valid SQLite database: {exc}")

##############################
# 2. Schema & data validation
##############################

def _get_products_schema(cursor):
    cursor.execute("PRAGMA table_info(products);")
    return [(row[1], row[2].upper(), row[5]) for row in cursor.fetchall()]
    # returns list of tuples: (name, type, is_pk)

def test_products_table_has_correct_schema_and_data():
    with sqlite3.connect(str(DB_FILE)) as conn:
        cur = conn.cursor()

        # Verify that the 'products' table exists exactly once.
        cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='products';"
        )
        tables = [row[0] for row in cur.fetchall()]
        assert tables == ["products"], (
            "The database must contain exactly one table named 'products'. "
            f"Found tables: {tables}"
        )

        # Verify schema: id INTEGER PRIMARY KEY, name TEXT, stock INTEGER
        schema = _get_products_schema(cur)
        expected_schema = [
            ("id", "INTEGER", 1),      # pk
            ("name", "TEXT", 0),
            ("stock", "INTEGER", 0),
        ]
        assert schema == expected_schema, (
            "The 'products' table schema is incorrect.\n"
            f"Expected: {expected_schema}\n"
            f"Found:    {schema}"
        )

        # Verify there are exactly three rows with the expected values.
        cur.execute("SELECT id, name, stock FROM products ORDER BY id;")
        rows = cur.fetchall()
        expected_rows = [
            (1, "wrench", 42),
            (2, "hammer", 17),
            (3, "screwdriver", 58),
        ]
        assert rows == expected_rows, (
            "The 'products' table must contain exactly the three rows specified "
            "in the task description.\n"
            f"Expected rows: {expected_rows}\n"
            f"Found rows:    {rows}"
        )

##############################
# 3. Ensure backup artefacts DO NOT exist yet
##############################

@pytest.mark.parametrize(
    "path",
    [BACKUP_SQL, BACKUP_GZ, BACKUP_SHA, BACKUP_LOG],
)
def test_no_backup_artefacts_exist_yet(path: Path):
    assert not path.exists(), (
        f"Found unexpected pre-existing file {path}. "
        "The backup procedure has not yet been run, so this file must be absent."
    )

##############################
# 4. If /home/user/backups exists, verify it is empty & has perms 755
##############################

def test_backup_directory_state_before_start():
    if BACKUP_DIR.exists():
        assert BACKUP_DIR.is_dir(), f"{BACKUP_DIR} exists but is not a directory."

        mode = BACKUP_DIR.stat().st_mode
        perms = stat.S_IMODE(mode)
        expected = 0o755
        assert perms == expected, (
            f"Directory {BACKUP_DIR} must have permissions {oct(expected)}, "
            f"but has {oct(perms)}."
        )

        # It should be empty; any files present would indicate the backup has
        # already been (partially) created.
        contents = [p.name for p in BACKUP_DIR.iterdir()]
        assert contents == [], (
            f"Backup directory {BACKUP_DIR} should be empty before the task starts, "
            f"but contains: {contents}"
        )