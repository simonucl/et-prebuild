# test_initial_state.py
#
# Pytest suite that verifies the initial filesystem state before the student
# runs the synchronisation command.  It intentionally avoids checking for the
# output paths (/home/user/backup/* or /home/user/etl_sync.log) because those
# are supposed to be created by the student’s command.

import pathlib
import pytest


ETL_DIR = pathlib.Path("/home/user/etl_data")

EXPECTED_FILES = {
    "customers.csv": (
        "id,name\n"
        "1,Alice\n"
        "2,Bob\n"
    ),
    "orders.csv": (
        "order_id,customer_id,amount\n"
        "1001,1,250.00\n"
        "1002,2,150.00\n"
    ),
    "readme.txt": "Sample ETL source data.\n",
}


def test_etl_data_directory_exists_and_is_dir():
    assert ETL_DIR.exists(), (
        f"Expected directory {ETL_DIR} to exist, but it does not."
    )
    assert ETL_DIR.is_dir(), (
        f"Expected {ETL_DIR} to be a directory, but it is not."
    )


def test_etl_data_contains_only_expected_files():
    # Collect names of files (skip sub-directories; their presence is a failure)
    found_files = set()
    unexpected_dirs = []

    for item in ETL_DIR.iterdir():
        if item.is_dir():
            unexpected_dirs.append(item.name)
        elif item.is_file():
            found_files.add(item.name)

    # Fail if any sub-directories are present
    assert not unexpected_dirs, (
        f"Found unexpected sub-directories inside {ETL_DIR}: {unexpected_dirs}. "
        "The directory should contain only the three source files and no sub-directories."
    )

    missing = set(EXPECTED_FILES) - found_files
    extra = found_files - set(EXPECTED_FILES)

    assert not missing, (
        f"The following expected file(s) are missing from {ETL_DIR}: {sorted(missing)}."
    )
    assert not extra, (
        f"Found unexpected extra file(s) in {ETL_DIR}: {sorted(extra)}. "
        "Only the files customers.csv, orders.csv, and readme.txt should be present."
    )


@pytest.mark.parametrize("filename,expected_content", EXPECTED_FILES.items())
def test_each_file_has_expected_content(filename, expected_content):
    file_path = ETL_DIR / filename
    assert file_path.exists(), f"Expected file {file_path} to exist, but it is missing."

    try:
        actual_content = file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        pytest.fail(f"Could not decode {file_path} as UTF-8: {exc}")

    assert actual_content == expected_content, (
        f"Contents of {file_path} do not match the expected contents.\n\n"
        f"Expected:\n{expected_content!r}\n\n"
        f"Found:\n{actual_content!r}"
    )