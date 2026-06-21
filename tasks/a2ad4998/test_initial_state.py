# test_initial_state.py
#
# This pytest suite validates the **initial** state of the filesystem
# _before_ the student performs any action.  It checks that:
#
# 1. The directory /home/user/migration_data exists.
# 2. The source TSV file exists and has the exact, expected header.
# 3. The source TSV file contains exactly eight data rows (nine lines total).
# 4. Exactly three rows have the status "migrate".
# 5. The two target artefacts do **not** yet exist.
#
# If any of these assertions fail, the error message will explain what is
# missing or unexpected.
#
# Only the Python standard library and `pytest` are used.

import pathlib
import pytest

MIGRATION_DIR = pathlib.Path("/home/user/migration_data")
SOURCE_FILE = MIGRATION_DIR / "services.tsv"
CSV_TARGET = MIGRATION_DIR / "services_to_migrate.csv"
LOG_TARGET = MIGRATION_DIR / "migration_summary.log"


def test_migration_directory_exists():
    assert MIGRATION_DIR.exists(), f"Required directory {MIGRATION_DIR} is missing."
    assert MIGRATION_DIR.is_dir(), f"{MIGRATION_DIR} exists but is not a directory."


def test_source_file_exists_and_header_is_correct():
    assert SOURCE_FILE.exists(), f"Source TSV file {SOURCE_FILE} is missing."
    assert SOURCE_FILE.is_file(), f"{SOURCE_FILE} exists but is not a regular file."

    # Read the first line (header) and validate exact columns
    with SOURCE_FILE.open("r", encoding="utf-8") as f:
        header = f.readline().rstrip("\n")

    expected_header = "\t".join(
        ["service_id", "service_name", "environment", "owner", "port", "status"]
    )
    assert (
        header == expected_header
    ), f"Header mismatch in {SOURCE_FILE}.\nExpected: {expected_header!r}\nFound:    {header!r}"


def test_source_file_has_expected_row_counts_and_statuses():
    with SOURCE_FILE.open("r", encoding="utf-8") as f:
        lines = [ln.rstrip("\n") for ln in f]

    # First line is header; remaining are data rows
    data_rows = lines[1:]

    assert (
        len(data_rows) == 8
    ), f"{SOURCE_FILE} should contain exactly 8 data rows; found {len(data_rows)}."

    # Ensure every data row has 6 TAB-separated fields
    for idx, row in enumerate(data_rows, start=2):  # start=2 to account for 1-based line numbers
        cols = row.split("\t")
        assert (
            len(cols) == 6
        ), f"Line {idx} of {SOURCE_FILE} should have 6 TAB-separated columns; found {len(cols)}."

    # Count rows with status == "migrate" (6th column)
    migrate_rows = [r for r in data_rows if r.split("\t")[5] == "migrate"]
    assert (
        len(migrate_rows) == 3
    ), f"Expected exactly 3 rows with status 'migrate'; found {len(migrate_rows)}."


def test_target_files_do_not_exist_yet():
    assert (
        not CSV_TARGET.exists()
    ), f"Target CSV {CSV_TARGET} should not exist before the student's commands are run."
    assert (
        not LOG_TARGET.exists()
    ), f"Target log {LOG_TARGET} should not exist before the student's commands are run."