# test_initial_state.py
#
# Pytest suite that asserts the **initial** filesystem state
# before the student performs the back-up task described in
# the assignment.  If any of these tests fail, the starting
# environment is not what the exercise expects.

import pathlib
import pytest

HOME = pathlib.Path("/home/user")
RAW_DIR = HOME / "projects/data_cleaning/raw_datasets"
ARCHIVE_DIR = HOME / "archive"
ARCHIVE_FILE = ARCHIVE_DIR / "raw_datasets_backup.tar.gz"
LOG_FILE = ARCHIVE_DIR / "backup_log.txt"


def test_raw_datasets_directory_exists_and_is_directory():
    """
    The raw_datasets directory must exist and be a directory.
    """
    assert RAW_DIR.exists(), (
        f"Directory '{RAW_DIR}' is missing.  "
        "The exercise expects it to exist before the back-up."
    )
    assert RAW_DIR.is_dir(), (
        f"'{RAW_DIR}' exists but is not a directory.  "
        "It must be a directory containing the CSV files."
    )


def test_raw_datasets_contains_exactly_expected_files():
    """
    The directory must contain exactly the three expected CSV files.
    """
    expected_files = {"sales_q1.csv", "sales_q2.csv", "customers.csv"}
    actual_files = {p.name for p in RAW_DIR.iterdir() if p.is_file()}
    missing = expected_files - actual_files
    unexpected = actual_files - expected_files

    assert not missing, (
        f"The following expected files are missing from '{RAW_DIR}': "
        f"{', '.join(sorted(missing))}"
    )
    assert not unexpected, (
        f"The directory '{RAW_DIR}' contains unexpected files: "
        f"{', '.join(sorted(unexpected))}"
    )


@pytest.mark.parametrize(
    "filename, expected_content",
    [
        ("sales_q1.csv", "id,amount\n1,100\n"),
        ("sales_q2.csv", "id,amount\n2,200\n"),
        ("customers.csv", "id,name\n1,Alice\n2,Bob\n"),
    ],
)
def test_each_csv_has_expected_contents(filename, expected_content):
    """
    Each CSV file must exist and contain the exact bytes specified
    in the assignment’s truth value.
    """
    file_path = RAW_DIR / filename
    assert file_path.is_file(), f"Expected file '{file_path}' to exist."
    actual_content = file_path.read_text(encoding="utf-8")
    assert (
        actual_content == expected_content
    ), f"Contents of '{file_path}' do not match the expected initial data."


def test_archive_file_does_not_yet_exist():
    """
    The gzip archive must NOT exist before the back-up is performed.
    """
    assert not ARCHIVE_FILE.exists(), (
        f"Archive file '{ARCHIVE_FILE}' already exists, "
        "but it should be created only after the student performs the task."
    )


def test_log_file_does_not_yet_exist():
    """
    The back-up log must NOT exist before the task is executed.
    """
    assert not LOG_FILE.exists(), (
        f"Log file '{LOG_FILE}' already exists, "
        "but it should be generated only after the student performs the task."
    )


def test_archive_directory_state_is_permissible():
    """
    /home/user/archive/ can be absent or an empty/writable directory.
    If it exists, ensure it's indeed a directory so subsequent commands won't fail.
    """
    if ARCHIVE_DIR.exists():
        assert ARCHIVE_DIR.is_dir(), (
            f"'{ARCHIVE_DIR}' exists but is not a directory.  "
            "It must either be absent (to be created later) or be a directory."
        )