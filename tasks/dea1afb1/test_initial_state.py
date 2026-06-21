# test_initial_state.py
#
# This pytest file verifies that the operating-system state *before*
# the student begins their work is exactly as expected.
#
# It checks ONLY pre-existing resources (inputs).  It does **not**
# look for any of the files that the student is supposed to create.

import os
from pathlib import Path

import pytest


CSV_PATH = Path("/home/user/slow_queries.csv")

# The exact CSV content that must already be present.
EXPECTED_CSV_CONTENT = (
    "query_id,db,username,duration_ms,sql_text\n"
    "1,inventory,alice,350,SELECT * FROM products;\n"
    "2,inventory,bob,1200,UPDATE products SET price = price*1.1 WHERE category='gadgets';\n"
    "3,hr,carol,900,SELECT * FROM employees WHERE salary > 70000;\n"
    "4,sales,dave,2400,DELETE FROM orders WHERE order_date < '2022-01-01';\n"
    "5,analytics,erin,1500,SELECT COUNT(*) FROM page_views WHERE view_date = CURRENT_DATE;\n"
)


@pytest.mark.parametrize("path", [CSV_PATH])
def test_file_exists(path):
    """
    Ensure that the required CSV file is present and is a regular file.
    """
    assert path.exists(), f"Required file {path} is missing."
    assert path.is_file(), f"Expected {path} to be a regular file."


def test_csv_contents_are_exact():
    """
    Verify that the CSV file contains exactly the expected bytes and is UTF-8 decodable.
    """
    # Read as bytes first to avoid any newline translation surprises.
    raw_bytes = CSV_PATH.read_bytes()

    try:
        contents = raw_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        pytest.fail(f"{CSV_PATH} is not valid UTF-8: {exc}")

    assert (
        contents == EXPECTED_CSV_CONTENT
    ), (
        f"{CSV_PATH} contents do not match the expected template.\n"
        "If you edited the file, restore it to the exact specification—"
        "including the final newline—and try again."
    )