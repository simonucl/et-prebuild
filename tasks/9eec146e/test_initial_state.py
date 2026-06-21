# test_initial_state.py
#
# Pytest suite to validate the starting condition for the
# “FinOps analyst” exercise _before_ the student performs any action.
#
# What we assert:
#   1. The /home/user/finops directory exists and is chmod 0755.
#   2. The SQLite database /home/user/finops/cloud_spend.db exists and is
#      chmod 0644 (or more permissive but not more restrictive).
#   3. The database contains a table `usage` with the exact schema
#         id       INTEGER  PRIMARY KEY
#         service  TEXT
#         month    TEXT
#         cost     REAL
#   4. The table is pre-populated with the five rows given in the
#      specification and their SUM(cost) for month = '2023-07' is 1024.57.
#
# NOTE:  We deliberately do NOT test for the existence (or absence) of
#        /home/user/finops/july_2023_total_cost.log because that is an
#        output artefact which the student will create.

import os
import stat
import sqlite3
import pytest

FINOPS_DIR = "/home/user/finops"
DB_PATH = os.path.join(FINOPS_DIR, "cloud_spend.db")

EXPECTED_DIR_MODE = 0o755
EXPECTED_DB_MODE  = 0o644

EXPECTED_SCHEMA = [
    ("id",      "INTEGER", 1),  # pk
    ("service", "TEXT",    0),
    ("month",   "TEXT",    0),
    ("cost",    "REAL",    0),
]

EXPECTED_ROWS = [
    (1, 'Compute Engine', '2023-07', 523.23),
    (2, 'Cloud Storage',  '2023-07', 123.45),
    (3, 'BigQuery',       '2023-07', 300.00),
    (4, 'Compute Engine', '2023-06', 200.00),
    (5, 'BigQuery',       '2023-07',  77.89),
]

@pytest.fixture(scope="module")
def connection():
    """Return a SQLite3 connection to the cloud_spend.db database."""
    if not os.path.exists(DB_PATH):
        pytest.skip(f"Database {DB_PATH} is missing; other tests will fail anyway.")
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
    finally:
        conn.close()

def mode_of(path):
    """Return the permission bits (e.g. 0o755) of a filesystem object."""
    return stat.S_IMODE(os.stat(path).st_mode)

def test_finops_directory_exists_and_permissions():
    assert os.path.isdir(FINOPS_DIR), \
        f"Expected directory {FINOPS_DIR} to exist."
    dir_mode = mode_of(FINOPS_DIR)
    assert dir_mode == EXPECTED_DIR_MODE, \
        f"{FINOPS_DIR} should have mode {oct(EXPECTED_DIR_MODE)}, found {oct(dir_mode)}."

def test_database_file_exists_and_permissions():
    assert os.path.isfile(DB_PATH), \
        f"Expected SQLite database file {DB_PATH} to exist."
    db_mode = mode_of(DB_PATH)
    # The spec requires 0644 *or less restrictive* (e.g. 0664, 0666)
    more_restrictive_than_expected = (db_mode & ~EXPECTED_DB_MODE) != 0
    assert not more_restrictive_than_expected, \
        (f"{DB_PATH} has mode {oct(db_mode)}, which is more restrictive than "
         f"the required {oct(EXPECTED_DB_MODE)} (must be world-readable).")

def test_schema_is_correct(connection):
    cur = connection.cursor()
    cur.execute("PRAGMA table_info(usage);")
    schema_info = cur.fetchall()  # CID, name, type, notnull, dflt_value, pk
    # Build a simpler representation: (name, type, pk_flag)
    simple_schema = [(row[1], row[2].upper(), row[5]) for row in schema_info]

    assert simple_schema == EXPECTED_SCHEMA, \
        ("Schema mismatch for table 'usage'.\n"
         f"Expected: {EXPECTED_SCHEMA}\n"
         f"Found:    {simple_schema}")

def test_seed_data_is_present(connection):
    cur = connection.cursor()
    cur.execute("SELECT * FROM usage ORDER BY id;")
    rows = cur.fetchall()
    assert rows == EXPECTED_ROWS, \
        ("Seed data in table 'usage' does not match the specification.\n"
         f"Expected rows:\n{EXPECTED_ROWS}\nFound rows:\n{rows}")

def test_sum_for_2023_07_is_correct(connection):
    cur = connection.cursor()
    cur.execute("SELECT SUM(cost) FROM usage WHERE month='2023-07';")
    (total,) = cur.fetchone()
    assert total == pytest.approx(1024.57, abs=1e-2), \
        (f"SUM(cost) for month='2023-07' expected to be 1024.57, "
         f"but got {total}.")