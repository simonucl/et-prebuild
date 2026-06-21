# test_initial_state.py
# Pytest suite that validates the pre-existing OS / filesystem state
# before the student performs any action.

import os
import stat
import sqlite3
import pytest

VULNSCAN_DIR = "/home/user/vulnscan"
DB_PATH = os.path.join(VULNSCAN_DIR, "scan_results.db")

# Expected rows as stored in the vulnerabilities table
EXPECTED_ROWS = [
    ("192.168.1.10", 22,   "ssh",   "CVE-2018-15473", "HIGH"),
    ("192.168.1.12", 80,   "http",  "CVE-2020-5902",  "HIGH"),
    ("192.168.1.20", 445,  "smb",   "CVE-2017-0144", "HIGH"),
    ("192.168.1.30", 21,   "ftp",   "CVE-2021-41617", "MEDIUM"),
    ("10.0.0.5",    3306, "mysql", "CVE-2016-6662",  "HIGH"),
]


def _mode_bits(path):
    """Return the permission bits (e.g. 0o755) of a path."""
    return stat.S_IMODE(os.stat(path).st_mode)


def test_vulnscan_directory_exists_and_permissions():
    """
    The directory /home/user/vulnscan must exist and have permissions 0755.
    """
    assert os.path.isdir(VULNSCAN_DIR), (
        f"Required directory {VULNSCAN_DIR} is missing."
    )

    perms = _mode_bits(VULNSCAN_DIR)
    assert perms == 0o755, (
        f"{VULNSCAN_DIR} should have permissions 755 "
        f"(rwxr-xr-x) but has {oct(perms)}"
    )


def test_scan_results_db_exists():
    """
    The SQLite database file must exist at the expected location.
    """
    assert os.path.isfile(DB_PATH), (
        f"Expected SQLite database {DB_PATH} is missing."
    )


def test_vulnerabilities_table_and_contents():
    """
    The database must contain a table named 'vulnerabilities' with exactly the
    five predefined rows (order does not matter).
    """
    # Connect using the stdlib sqlite3 module
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()

        # 1. Confirm the table exists
        cur.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type='table' AND name='vulnerabilities';"
        )
        table = cur.fetchone()
        assert table is not None, (
            "Table 'vulnerabilities' is missing from the database."
        )

        # 2. Fetch all rows and compare to expected
        cur.execute(
            "SELECT host_ip, port, service, cve_id, severity "
            "FROM vulnerabilities;"
        )
        rows = cur.fetchall()

        # Sort both lists for comparison irrespective of row order
        rows_sorted = sorted(rows)
        expected_sorted = sorted(EXPECTED_ROWS)

        assert rows_sorted == expected_sorted, (
            "Contents of the 'vulnerabilities' table do not match the expected "
            "data.\n\n"
            f"Expected rows ({len(EXPECTED_ROWS)}):\n{expected_sorted}\n\n"
            f"Actual rows ({len(rows)}):\n{rows_sorted}"
        )

    finally:
        conn.close()