# test_initial_state.py
# Pytest suite to validate the initial filesystem state
#
# This file asserts that the data needed for the exercise is present
# and correct *before* the student performs any actions.
#
# Rules honoured:
#   • Uses only stdlib + pytest
#   • Does NOT test for any of the output files or directories
#   • Fails give clear, instructive messages

import os
import pytest

HOME = "/home/user"
WEBDEV_DIR = os.path.join(HOME, "webdev")
DATA_DIR = os.path.join(WEBDEV_DIR, "data")
PRODUCTS_CSV = os.path.join(DATA_DIR, "products.csv")


@pytest.fixture(scope="module")
def products_csv_bytes():
    """Return the raw bytes of products.csv (or fail early if unreadable)."""
    if not os.path.exists(PRODUCTS_CSV):
        pytest.fail(f"Required file missing: {PRODUCTS_CSV}")

    try:
        with open(PRODUCTS_CSV, "rb") as f:
            return f.read()
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Unable to read {PRODUCTS_CSV}: {exc}")


def test_required_directories_exist():
    """Ensure /home/user/webdev and /home/user/webdev/data exist."""
    assert os.path.isdir(WEBDEV_DIR), f"Directory missing: {WEBDEV_DIR}"
    assert os.path.isdir(DATA_DIR), f"Directory missing: {DATA_DIR}"


def test_products_csv_exists_and_readable():
    """Basic existence & readability check for products.csv."""
    assert os.path.isfile(PRODUCTS_CSV), f"File missing: {PRODUCTS_CSV}"
    assert os.access(PRODUCTS_CSV, os.R_OK), f"File not readable: {PRODUCTS_CSV}"


def test_products_csv_exact_content(products_csv_bytes):
    """
    The CSV must exactly match the expected content, byte-for-byte,
    including the trailing LF newline on the final line.
    """
    expected = (
        b"id,name,price,status\n"
        b"1,Widget,19.99,active\n"
        b"2,Gadget,29.49,discontinued\n"
        b"3,Doohickey,9.95,active\n"
        b"4,Thingamajig,4.50,discontinued\n"
        b"5,Whatsit,14.00,active\n"
    )
    assert (
        products_csv_bytes == expected
    ), (
        "The contents of products.csv do not match the expected initial data.\n"
        "If the file was modified or corrupted, restore it to exactly the "
        "following (each line ends with LF '\\n'):\n\n"
        + expected.decode()
    )