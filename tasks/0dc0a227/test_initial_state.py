# test_initial_state.py
#
# This pytest suite validates the state of the filesystem *before*
# the student performs any actions.  It checks that the starting CSV
# file exists with the exact expected contents and that none of the
# target output files are present yet.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
DOCS = HOME / "docs"

SOURCE_CSV = DOCS / "source_documentation.csv"
TARGET_TSV = DOCS / "endpoint_method.tsv"
CREATION_LOG = DOCS / "creation.log"

EXPECTED_CSV_CONTENT = (
    "endpoint,method,description,author\n"
    "/users,GET,Retrieve all users,alice\n"
    "/users,POST,Create a user,bob\n"
    "/orders,GET,Retrieve all orders,carol\n"
)


def test_source_csv_exists():
    """Verify that the starting CSV file exists and is a regular file."""
    assert SOURCE_CSV.exists(), (
        f"Expected source CSV file '{SOURCE_CSV}' does not exist."
    )
    assert SOURCE_CSV.is_file(), (
        f"Expected '{SOURCE_CSV}' to be a regular file, "
        f"but it is not (might be a directory or symlink)."
    )


def test_source_csv_content():
    """Verify that the starting CSV file has the exact expected content."""
    actual = SOURCE_CSV.read_text(encoding="utf-8")
    assert actual == EXPECTED_CSV_CONTENT, (
        "The content of '{file}' is not as expected.\n\n"
        "Expected (repr):\n{expected!r}\n\n"
        "Actual (repr):\n{actual!r}\n".format(
            file=SOURCE_CSV, expected=EXPECTED_CSV_CONTENT, actual=actual
        )
    )


@pytest.mark.parametrize(
    "path,description",
    [
        (TARGET_TSV, "output TSV"),
        (CREATION_LOG, "creation log"),
    ],
)
def test_output_files_do_not_exist_yet(path: Path, description: str):
    """Ensure that the expected output files are NOT present before the task."""
    assert not path.exists(), (
        f"The {description} file '{path}' should not exist before the student "
        f"performs the required actions."
    )