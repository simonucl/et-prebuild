# test_initial_state.py
"""
Pytest suite that validates the **initial** (already-provisioned) state
of the filesystem and SQLite database for the “mobile build audit” task.

The checks assert that:
1. Mandatory directories / files already exist.
2. The SQLite schema matches the specification exactly.
3. The required seed data are present and in the correct order.
4. The human-readable summary report is present and byte-perfect.

These tests are run **before** the student begins writing any code so that
the grading system is sure the starting point is correct and reproducible.
"""

import os
import sqlite3
import pytest

HOME = "/home/user"
PIPELINES_DIR = os.path.join(HOME, "mobile_pipelines")
DB_PATH = os.path.join(PIPELINES_DIR, "builds.db")
REPORT_DIR = os.path.join(PIPELINES_DIR, "report")
SUMMARY_LOG = os.path.join(REPORT_DIR, "build_summary.log")


# --------------------------------------------------------------------------- #
# Helpers                                                                     #
# --------------------------------------------------------------------------- #
def _read_file_bytes(path: str) -> bytes:
    """Read a file in binary mode, raising a helpful assertion if it fails."""
    assert os.path.isfile(path), f"Expected file at '{path}' to exist."
    with open(path, "rb") as fh:
        return fh.read()


def _collect_table_info(conn: sqlite3.Connection, table: str):
    """
    Return a list of (cid, name, type, notnull, dflt_value, pk) rows
    from PRAGMA table_info, ordered by cid.
    """
    cur = conn.execute(f"PRAGMA table_info({table})")
    return cur.fetchall()


# --------------------------------------------------------------------------- #
# Filesystem checks                                                           #
# --------------------------------------------------------------------------- #
def test_required_directories_exist():
    assert os.path.isdir(
        PIPELINES_DIR
    ), f"Directory '{PIPELINES_DIR}' is missing; it must already exist."
    assert os.path.isdir(
        REPORT_DIR
    ), f"Directory '{REPORT_DIR}' is missing; it must already exist."


def test_required_files_exist():
    assert os.path.isfile(
        DB_PATH
    ), f"SQLite database '{DB_PATH}' is missing; it must already exist."
    assert os.path.isfile(
        SUMMARY_LOG
    ), f"Summary log '{SUMMARY_LOG}' is missing; it must already exist."


# --------------------------------------------------------------------------- #
# SQLite schema and data checks                                               #
# --------------------------------------------------------------------------- #
@pytest.fixture(scope="module")
def db_conn():
    """Return a read-only SQLite connection to the builds.db database."""
    uri = f"file:{DB_PATH}?mode=ro"
    try:
        conn = sqlite3.connect(uri, uri=True)
    except sqlite3.Error as exc:
        pytest.fail(f"Unable to open SQLite database '{DB_PATH}': {exc}")
    yield conn
    conn.close()


def test_schema_builds_table(db_conn):
    expected_columns = [
        (0, "id", "INTEGER", 0, None, 1),
        (1, "commit_hash", "TEXT", 1, None, 0),
        (2, "status", "TEXT", 1, None, 0),
        (3, "duration_sec", "INTEGER", 1, None, 0),
        (4, "timestamp", "TEXT", 1, None, 0),
    ]
    info = _collect_table_info(db_conn, "builds")
    assert info == expected_columns, (
        "Schema mismatch for table 'builds'.\n"
        f"Expected columns:\n{expected_columns}\nGot:\n{info}"
    )


def test_schema_artifacts_table(db_conn):
    expected_columns = [
        (0, "id", "INTEGER", 0, None, 1),
        (1, "build_id", "INTEGER", 1, None, 0),
        (2, "artifact_name", "TEXT", 1, None, 0),
        (3, "size_kb", "INTEGER", 1, None, 0),
    ]
    info = _collect_table_info(db_conn, "artifacts")
    assert info == expected_columns, (
        "Schema mismatch for table 'artifacts'.\n"
        f"Expected columns:\n{expected_columns}\nGot:\n{info}"
    )


def test_seed_rows_in_builds(db_conn):
    cur = db_conn.execute("SELECT * FROM builds ORDER BY id;")
    rows = cur.fetchall()
    expected = [
        (1, "a1b2c3d4", "SUCCESS", 320, "2023-09-01T12:01:30Z"),
        (2, "e5f6g7h8", "FAILED", 150, "2023-09-02T14:22:10Z"),
        (3, "i9j0k1l2", "SUCCESS", 287, "2023-09-03T09:47:55Z"),
    ]
    assert rows == expected, (
        "Rows in 'builds' do not match the required seed data.\n"
        f"Expected:\n{expected}\nGot:\n{rows}"
    )


def test_seed_rows_in_artifacts(db_conn):
    cur = db_conn.execute("SELECT * FROM artifacts ORDER BY id;")
    rows = cur.fetchall()
    expected = [
        (1, 1, "app-release.apk", 20480),
        (2, 1, "symbols.zip", 5120),
        (3, 2, "crash-log.txt", 12),
        (4, 3, "app-release.apk", 20512),
    ]
    assert rows == expected, (
        "Rows in 'artifacts' do not match the required seed data.\n"
        f"Expected:\n{expected}\nGot:\n{rows}"
    )


# --------------------------------------------------------------------------- #
# Report content check                                                        #
# --------------------------------------------------------------------------- #
def test_build_summary_log_content(db_conn):
    expected_content = (
        b"Build Summary Report\n"
        b"\n"
        b"Commit Hash | Status   | Artifact Count\n"
        b"----------------------------------------\n"
        b"a1b2c3d4     | SUCCESS  | 2\n"
        b"e5f6g7h8     | FAILED   | 1\n"
        b"i9j0k1l2     | SUCCESS  | 1\n"
    )
    file_bytes = _read_file_bytes(SUMMARY_LOG)
    assert (
        file_bytes == expected_content
    ), "build_summary.log content does not match the expected report."

    # Extra safety: ensure the SQL query behind the report is correct
    query = """
        SELECT commit_hash,
               status,
               COUNT(artifacts.id) AS artifact_count
        FROM   builds
        LEFT JOIN artifacts ON builds.id = artifacts.build_id
        GROUP  BY builds.id
        ORDER  BY builds.id;
    """
    cur = db_conn.execute(query)
    generated_rows = cur.fetchall()
    expected_rows = [
        ("a1b2c3d4", "SUCCESS", 2),
        ("e5f6g7h8", "FAILED", 1),
        ("i9j0k1l2", "SUCCESS", 1),
    ]
    assert generated_rows == expected_rows, (
        "The SQL query result does not match the data in the report.\n"
        f"Expected rows:\n{expected_rows}\nGot:\n{generated_rows}"
    )