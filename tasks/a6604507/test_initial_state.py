# test_initial_state.py
"""
Pytest suite to verify the operating-system / filesystem state
*before* the student performs any actions for the “clean customers CSV”
exercise.

What we validate:
1. /home/user/data/raw/customers.csv
   • must exist as a regular file
   • must have exactly the expected contents (including the
     final trailing newline)
   • must have 0o644 permissions

2. /home/user/data/clean            MUST NOT exist yet.
3. /home/user/data/clean/customers_clean.csv MUST NOT exist yet.

If any of these pre-conditions fail, the tests raise clear,
actionable assertion messages.
"""
import os
import stat
import textwrap

RAW_FILE_PATH = "/home/user/data/raw/customers.csv"
CLEAN_DIR_PATH = "/home/user/data/clean"
CLEAN_FILE_PATH = os.path.join(CLEAN_DIR_PATH, "customers_clean.csv")

# Expected exact contents of the raw file (including final newline)
EXPECTED_RAW_CONTENT = (
    "customer_id,first_name,last_name,email,age\n"
    "1,John,Doe,john.doe@example.com,28\n"
    "2,Jane,NULL,jane@example.com,34\n"
    "3,Bob,Smith,NULL,45\n"
    "4,Anna,Adams,anna.adams@example.com,31\n"
    "5,NULL,White,white@example.com,27\n"
    "6,Mark,Brown,mark.brown@example.com,NULL\n"
)


def _file_mode(path: str) -> int:
    """Return the permission bits (e.g. 0o644) for *path*."""
    return stat.S_IMODE(os.stat(path).st_mode)


def test_raw_customers_file_exists_and_is_regular_file():
    assert os.path.isfile(
        RAW_FILE_PATH
    ), f"Required file missing: {RAW_FILE_PATH!r}. It must exist before you begin the task."


def test_raw_customers_file_permissions():
    mode = _file_mode(RAW_FILE_PATH)
    expected_mode = 0o644
    assert (
        mode == expected_mode
    ), (
        f"Unexpected permissions on {RAW_FILE_PATH!r}: "
        f"got octal {oct(mode)}, expected {oct(expected_mode)}."
    )


def test_raw_customers_file_contents_exact_match():
    with open(RAW_FILE_PATH, "r", encoding="utf-8") as fp:
        actual = fp.read()

    assert (
        actual == EXPECTED_RAW_CONTENT
    ), textwrap.dedent(
        f"""
        The contents of {RAW_FILE_PATH!r} do not match the expected
        initial dataset.  Any difference—even extra spaces or missing
        newlines—will cause this task to be graded incorrectly.

        --- Expected (exact) ---
        {EXPECTED_RAW_CONTENT}
        ---   Got   ---
        {actual}
        ------------------------
        """
    )


def test_clean_directory_does_not_exist_yet():
    assert not os.path.exists(
        CLEAN_DIR_PATH
    ), (
        f"The directory {CLEAN_DIR_PATH!r} already exists, but it must "
        f"NOT be present before the task begins.  Remove it and start over."
    )


def test_clean_customers_file_does_not_exist_yet():
    assert not os.path.exists(
        CLEAN_FILE_PATH
    ), (
        f"The cleaned CSV {CLEAN_FILE_PATH!r} already exists, but it must "
        f"NOT exist before the task begins."
    )