# test_initial_state.py
#
# Pytest suite that validates the *starting* filesystem / OS state for the
# “SQLite query-tuning” exercise **before** the student makes any changes.
#
# These tests purposefully FAIL if something that the student is supposed
# to create (e.g. the optimisation log or the required indexes) is already
# present, or if any of the pre-seeded artefacts are missing / malformed.
#
# Standard library only + pytest, no third-party deps.

import os
import stat
import sqlite3
import textwrap
import pytest
from pathlib import Path

HOME = Path("/home/user")
DB_PATH = HOME / "sales.db"
SQL_PATH = HOME / "queries.sql"
RUNNER_PATH = HOME / "run_query.sh"


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def _read_queries_sql():
    """Return the content of queries.sql as a list of stripped lines."""
    with SQL_PATH.open("r", encoding="utf-8") as fh:
        return [line.rstrip("\n") for line in fh]


def _connect_db():
    """Return an sqlite3.Connection to /home/user/sales.db in read-only mode."""
    # Using URI with immutable=1 protects against accidental writes
    uri = f"file:{DB_PATH}?mode=ro&immutable=1"
    return sqlite3.connect(uri, uri=True)


# --------------------------------------------------------------------------- #
# Actual tests
# --------------------------------------------------------------------------- #

def test_sales_db_exists_and_is_readable():
    assert DB_PATH.is_file(), f"Database file expected at {DB_PATH} but not found."
    assert os.access(DB_PATH, os.R_OK), f"Database file {DB_PATH} is not readable."


def test_sales_db_schema_and_rowcounts():
    """
    Verify that the two expected tables exist with the correct columns and that
    the seed row counts match what the instructions describe.
    """
    expected_tables = {
        "customers": ["id", "name"],
        "orders": ["id", "customer_id", "order_total", "order_date"],
    }

    with _connect_db() as conn:
        cur = conn.cursor()

        # 1. Tables present
        cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table';"
        )
        tables_in_db = {row[0] for row in cur.fetchall()}
        for tbl in expected_tables:
            assert (
                tbl in tables_in_db
            ), f"Expected table '{tbl}' not found in {DB_PATH}; found {tables_in_db}."

        # 2. Columns correct
        for tbl, cols in expected_tables.items():
            cur.execute(f"PRAGMA table_info('{tbl}')")
            cols_in_db = [row[1] for row in cur.fetchall()]
            assert cols_in_db == cols, (
                f"Table '{tbl}' has columns {cols_in_db}, "
                f"but expected exactly {cols} (order matters)."
            )

        # 3. Row counts
        cur.execute("SELECT COUNT(*) FROM customers")
        customers_cnt = cur.fetchone()[0]
        assert customers_cnt == 100, (
            f"Expected 100 customer rows but found {customers_cnt}."
        )

        cur.execute("SELECT COUNT(*) FROM orders")
        orders_cnt = cur.fetchone()[0]
        assert orders_cnt == 50_000, (
            f"Expected 50,000 order rows but found {orders_cnt}."
        )


def test_no_preexisting_indexes():
    """
    Ensure the two performance indexes the student must create do *not* exist
    yet; otherwise the optimisation exercise is pointless.
    """
    forbidden_indexes = {
        "idx_orders_customer_id",
        "idx_orders_order_date",
    }
    with _connect_db() as conn:
        cur = conn.cursor()
        cur.execute("PRAGMA index_list('orders');")
        existing = {row[1] for row in cur.fetchall()}  # row[1] = index name

    intersection = existing & forbidden_indexes
    assert not intersection, textwrap.dedent(
        f"""
        The following index(es) already exist in the starter database: {sorted(intersection)}.
        They must NOT be present before the student begins the optimisation task.
        """
    )


def test_queries_sql_exists_and_contains_two_named_queries():
    assert SQL_PATH.is_file(), f"Expected SQL file {SQL_PATH} but it is missing."

    lines = _read_queries_sql()
    names = [ln.split("name:", 1)[1].strip()  # extract the tag contents
             for ln in lines if ln.strip().startswith("-- name:")]

    expected = ["top_customers", "monthly_revenue"]
    assert names == expected, (
        f"{SQL_PATH} should contain the two query tags {expected} "
        f"in that exact order. Found tags: {names}"
    )


def test_run_query_helper_script_exists_and_is_executable():
    assert RUNNER_PATH.is_file(), f"Helper script {RUNNER_PATH} is missing."
    st = RUNNER_PATH.stat()
    is_executable = bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
    assert is_executable, f"Helper script {RUNNER_PATH} exists but is not executable."


# --------------------------------------------------------------------------- #
# The following test purposefully ensures that the optimisation log does NOT
# yet exist.  The student will create it during the assignment.  If the file
# is already present the initial state is considered invalid.
# --------------------------------------------------------------------------- #

def test_optimisation_log_not_yet_created():
    log_path = HOME / "query_optimization.log"
    assert not log_path.exists(), (
        f"{log_path} is already present, but it should be created only after "
        "the optimisation work is completed."
    )