# test_initial_state.py
#
# This pytest suite validates the **initial** state of the filesystem and the
# SQLite database *before* the student begins any work.  It purposefully does
# NOT look for the final artefacts the assignment asks the student to create
# (e.g. the change-log file).  If any of these tests fail, the starting
# environment is incorrect.

import os
import sqlite3
import pytest

DB_PATH = "/home/user/projects/i18n/messages.db"


@pytest.fixture(scope="module")
def db_connection():
    """
    Yields a read-only SQLite connection to the messages.db file.
    The DB must already exist; if it doesn't, the test suite will fail
    with a clear message.
    """
    if not os.path.isfile(DB_PATH):
        pytest.fail(
            f"Expected database file at {DB_PATH!r} to exist, "
            "but it was not found."
        )

    # `uri=True` lets us open the DB in read-only mode to guarantee we do not
    # mutate it during testing.
    uri = f"file:{DB_PATH}?mode=ro"
    try:
        conn = sqlite3.connect(uri, uri=True, timeout=5)
    except sqlite3.OperationalError as exc:
        pytest.fail(f"Unable to open the SQLite database in read-only mode: {exc}")
    try:
        yield conn
    finally:
        conn.close()


def test_translations_table_exists(db_connection):
    cur = db_connection.cursor()
    cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='translations';"
    )
    row = cur.fetchone()
    assert row is not None, (
        "Table 'translations' is missing from the database. "
        "The initial schema should contain this table."
    )


def test_translations_table_schema(db_connection):
    """
    Validates that the 'translations' table contains exactly the four expected
    columns with the correct names *in the correct order* and that the primary
    key is on the 'id' column.
    """
    cur = db_connection.cursor()
    cur.execute("PRAGMA table_info(translations);")
    columns = cur.fetchall()

    # Expected PRAGMA layout: (cid, name, type, notnull, dflt_value, pk)
    expected = [
        (0, "id", "INTEGER", 0, None, 1),         # PRIMARY KEY
        (1, "language", "TEXT", 1, None, 0),
        (2, "key", "TEXT", 1, None, 0),
        (3, "value", "TEXT", 1, None, 0),
    ]

    # We only compare the attributes we care about: index, name, type, pk flag.
    simplified_actual   = [(c[0], c[1], c[2].upper(), c[5]) for c in columns]
    simplified_expected = [(c[0], c[1], c[2], c[5])          for c in expected]

    assert simplified_actual == simplified_expected, (
        "Unexpected schema for table 'translations'.\n"
        f"Actual PRAGMA output:\n  {columns}\n"
        f"Expected (cid, name, type, pk):\n  {simplified_expected}"
    )


def test_initial_rows(db_connection):
    """
    Confirms that the database starts with EXACTLY two rows:
        1 | en | hello   | Hello
        2 | en | goodbye | Goodbye
    and nothing else.
    """
    cur = db_connection.cursor()
    cur.execute(
        "SELECT id, language, key, value FROM translations ORDER BY id;"
    )
    rows = cur.fetchall()

    expected_rows = [
        (1, "en", "hello", "Hello"),
        (2, "en", "goodbye", "Goodbye"),  # Note: no space!
    ]

    assert rows == expected_rows, (
        "The initial contents of the 'translations' table do not match the "
        "required starting state.\n"
        f"Actual rows ({len(rows)}):\n  {rows}\n"
        f"Expected ({len(expected_rows)}):\n  {expected_rows}"
    )