# test_initial_state.py
#
# This pytest suite validates the **initial** filesystem state that must be
# present **before** the student performs any migration steps for the
# “legacy-customer extract” exercise.
#
# Nothing in here checks for the *output* artefacts that the student will
# have to create later; those are deliberately left untested at this stage.

import os
import pytest

HOME = "/home/user"
SOURCE_DIR = os.path.join(HOME, "data", "source")
LEGACY_FILE = os.path.join(SOURCE_DIR, "customers_legacy.csv")

EXPECTED_LEGACY_LINES = [
    "customer_id,name,age,signup_date",
    "1,Alice,30,2021-01-05",
    "2,Bob,17,2022-07-12",
    "3,Charlie,25,2019-11-23",
    "4,David,15,2020-02-14",
    "5,Eva,40,2018-06-30",
    "6,Frank,22,2023-03-01",
]


def test_home_directory_exists():
    """Sanity-check: the user’s home directory must exist."""
    assert os.path.isdir(HOME), f"Expected {HOME} to exist and be a directory."


def test_source_directory_exists():
    """The legacy data folder must be present."""
    assert os.path.isdir(
        SOURCE_DIR
    ), f"Missing source directory: expected path {SOURCE_DIR!r}."


def test_legacy_file_exists():
    """The CSV with legacy customer data must be present."""
    assert os.path.isfile(
        LEGACY_FILE
    ), f"Missing legacy CSV file: expected path {LEGACY_FILE!r}."


def test_legacy_file_contents_exact():
    """
    The legacy CSV must contain the exact, unmodified data provided
    in the task description (UTF-8, LF line endings, header first).
    """
    # Read file in text mode using UTF-8; this will raise if encoding is wrong.
    with open(LEGACY_FILE, "r", encoding="utf-8", newline="\n") as fh:
        # .splitlines() keeps all logical lines but discards the trailing '\n'.
        actual_lines = fh.read().splitlines()

    # Provide a clear diff if something is off.
    assert actual_lines == EXPECTED_LEGACY_LINES, (
        "The contents of the legacy CSV do not match the expected data.\n"
        "Expected:\n"
        + "\n".join(EXPECTED_LEGACY_LINES)
        + "\n\nActual:\n"
        + "\n".join(actual_lines)
    )


def test_legacy_file_line_endings_are_LF():
    """
    Ensure the file uses Unix LF line endings only.
    Windows CRLF sequences are *not* allowed.
    """
    with open(LEGACY_FILE, "rb") as fh:
        content = fh.read()

    assert b"\r\n" not in content, (
        f"The file {LEGACY_FILE!r} contains CRLF (\\r\\n) line endings; "
        "only LF (\\n) line endings are allowed."
    )