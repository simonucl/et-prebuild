# test_initial_state.py
#
# This test-suite validates that the *initial* filesystem and database
# state matches the expectations described in the assignment.  It
# intentionally does **not** test for the presence of any files that
# the learner is supposed to create later (e.g. /home/user/destination.db
# or /home/user/migration_validation.log).

import os
import sqlite3
import textwrap
import pytest

SOURCE_DB = "/home/user/source.db"

# Expected schema (as stored in sqlite_master.sql – no trailing semicolon).
EXPECTED_SCHEMA = textwrap.dedent(
    """
    CREATE TABLE network_logs(
      id INTEGER PRIMARY KEY,
      timestamp TEXT,
      src_ip TEXT,
      dest_ip TEXT,
      action TEXT
    )
    """
).strip()

# Expected full contents of the table.
EXPECTED_ROWS = [
    (1, "2023-06-01T12:00:00Z", "10.0.0.5",  "192.168.1.20", "ALLOW"),
    (2, "2023-06-01T12:05:00Z", "10.0.0.5",  "172.16.0.8",   "ALLOW"),
    (3, "2023-06-01T12:10:00Z", "10.0.0.10", "192.168.1.21", "DENY"),
    (4, "2023-06-01T12:15:00Z", "10.0.0.15", "192.168.1.22", "ALLOW"),
    (5, "2023-06-01T12:20:00Z", "10.0.0.20", "192.168.1.23", "DENY"),
]


@pytest.fixture(scope="module")
def conn():
    """Return a read-only connection to the source database."""
    assert os.path.isfile(
        SOURCE_DB
    ), f"Expected source database at {SOURCE_DB!r} but it does not exist."
    # Open in read-only mode to protect the evidence file.
    uri = f"file:{SOURCE_DB}?mode=ro"
    return sqlite3.connect(uri, uri=True)


def test_network_logs_table_exists(conn):
    """The source DB must contain exactly one table called network_logs."""
    cur = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='network_logs';"
    )
    names = [row[0] for row in cur.fetchall()]
    assert names == ["network_logs"], (
        "Table 'network_logs' is missing from the source database; "
        f"found tables: {names}"
    )


def _normalized(sql: str) -> str:
    """Minify SQL by removing all whitespace so tiny formatting differences don't matter."""
    return "".join(sql.split()).lower()


def test_network_logs_schema(conn):
    """Schema of network_logs must match the expected definition exactly."""
    cur = conn.execute(
        "SELECT sql FROM sqlite_master WHERE type='table' AND name='network_logs';"
    )
    row = cur.fetchone()
    assert row is not None, "Could not retrieve schema for 'network_logs'."
    actual_schema = row[0]
    assert (
        _normalized(actual_schema) == _normalized(EXPECTED_SCHEMA)
    ), f"Schema mismatch.\nExpected:\n{EXPECTED_SCHEMA}\n\nActual:\n{actual_schema}"


def test_network_logs_row_count(conn):
    """network_logs must contain exactly five rows."""
    cur = conn.execute("SELECT COUNT(*) FROM network_logs;")
    (count,) = cur.fetchone()
    assert count == 5, f"Expected 5 rows in 'network_logs', found {count}."


def test_network_logs_row_contents(conn):
    """All rows and their order must match the expected dataset."""
    cur = conn.execute(
        "SELECT id, timestamp, src_ip, dest_ip, action FROM network_logs ORDER BY id;"
    )
    rows = cur.fetchall()
    assert rows == EXPECTED_ROWS, (
        "Table 'network_logs' does not contain the expected data.\n\n"
        f"Expected rows:\n{EXPECTED_ROWS}\n\nActual rows:\n{rows}"
    )