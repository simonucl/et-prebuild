# test_initial_state.py
#
# Pytest suite to validate the initial file-system state *before* the student
# begins any work on the “Database dumps cleanup” task.  These tests are meant
# to be executed immediately after the exercise is provisioned.  They confirm
# that the required source files are present, and that no artefacts the
# student is supposed to create already exist.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
DB_DUMPS_DIR = HOME / "db_dumps"
BACKUPS_DIR = HOME / "backups"
DB_WORK_DIR = HOME / "db_work"

CUSTOMERS_SQL = DB_DUMPS_DIR / "customers.sql"
ORDERS_SQL = DB_DUMPS_DIR / "orders.sql"
INVENTORY_SQL = DB_DUMPS_DIR / "inventory.sql"

# --------------------------------------------------------------------------- #
# Expected file contents (verbatim, including newlines at the end of file).   #
# --------------------------------------------------------------------------- #

EXPECTED_CUSTOMERS = (
    "-- Dump of table customers\n"
    "INSERT INTO customers (id, name, email) VALUES\n"
    "(1, 'Alice Smith', 'alice@example.com'),\n"
    "(2, 'Bob Jones', 'bob@example.com');\n"
)

EXPECTED_ORDERS = (
    "-- Dump of table orders\n"
    "INSERT INTO orders (id, customer_id, order_total) VALUES\n"
    "(1, 1, 99.99),\n"
    "(2, 2, 149.49);\n"
)

EXPECTED_INVENTORY = (
    "-- Dump of table inventory\n"
    "INSERT INTO inventory (id, product_name, quantity) VALUES\n"
    "(1, 'Widget', 500),\n"
    "(2, 'Gadget', 300);\n"
)


# --------------------------------------------------------------------------- #
# Helper functions                                                            #
# --------------------------------------------------------------------------- #

def read_text_file(path: Path) -> str:
    """Read a UTF-8 text file and return its full contents."""
    with path.open("r", encoding="utf-8") as f:
        return f.read()


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #

def test_db_dumps_directory_exists():
    assert DB_DUMPS_DIR.is_dir(), (
        f"Expected directory {DB_DUMPS_DIR} does not exist. "
        "The starting condition requires it to be present."
    )


@pytest.mark.parametrize(
    "file_path,expected_content",
    [
        (CUSTOMERS_SQL, EXPECTED_CUSTOMERS),
        (ORDERS_SQL, EXPECTED_ORDERS),
        (INVENTORY_SQL, EXPECTED_INVENTORY),
    ],
)
def test_sql_files_exist_with_correct_content(file_path: Path, expected_content: str):
    assert file_path.is_file(), (
        f"Missing required file: {file_path}. "
        "All three .sql files must be present in /home/user/db_dumps."
    )

    actual_content = read_text_file(file_path)
    # Compare *exact* content after stripping trailing whitespace at EOF to
    # avoid issues with editors that may or may not add a final newline.
    assert actual_content.strip() == expected_content.strip(), (
        f"Content mismatch in {file_path}.\n\n"
        "Expected:\n"
        f"{expected_content!r}\n\n"
        "Actual:\n"
        f"{actual_content!r}"
    )


def test_output_directories_do_not_yet_exist():
    # None of the artefacts the student must create should be present at the
    # start of the exercise.
    for path in (BACKUPS_DIR, DB_WORK_DIR):
        assert not path.exists(), (
            f"The directory {path} already exists, but it should NOT be present "
            "before the student begins the task."
        )

    # Also make sure the archive and checksum files are absent.
    archive = BACKUPS_DIR / "db_dumps_backup.tar.gz"
    checksum = BACKUPS_DIR / "db_dumps_backup.sha256"
    orders_copy = DB_WORK_DIR / "orders.sql"
    extraction_log = DB_WORK_DIR / "extraction.log"

    for file_path in (archive, checksum, orders_copy, extraction_log):
        assert not file_path.exists(), (
            f"The file {file_path} should not exist at the initial state."
        )