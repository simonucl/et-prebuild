# test_initial_state.py
#
# Pytest suite that validates the **initial** filesystem / OS state
# before the student modifies anything.  The tests deliberately avoid
# looking for the output files that will be created later; they only
# assert the presence and correctness of the *given* resources.

import os
import stat
import pytest

HOME = "/home/user"
RAW_DIR = os.path.join(HOME, "data", "raw")
PROCESSED_DIR = os.path.join(HOME, "data", "processed")
PROJECT_DIR = os.path.join(HOME, "project")
SCRIPT_PATH = os.path.join(PROJECT_DIR, "process_data.sh")

RAW_FILES = {
    "sales_q1.csv": (
        "id,region,amount\n"
        "1,North,1000\n"
        "2,South,1500\n"
        "3,East,800\n"
    ),
    "sales_q2.csv": (
        "id,region,amount\n"
        "4,North,1100\n"
        "5,South,1600\n"
        "6,West,900\n"
    ),
    "sales_q3.csv": (
        "id,region,amount\n"
        "7,East,1200\n"
        "8,West,950\n"
        "9,North,1300\n"
    ),
}


def test_directory_layout_exists():
    """Verify that the expected directory tree is present."""
    # /home/user/data/raw
    assert os.path.isdir(
        RAW_DIR
    ), f"Required directory missing: {RAW_DIR}"
    # /home/user/data/processed
    assert os.path.isdir(
        PROCESSED_DIR
    ), f"Required directory missing: {PROCESSED_DIR}"
    # /home/user/project
    assert os.path.isdir(
        PROJECT_DIR
    ), f"Required directory missing: {PROJECT_DIR}"


@pytest.mark.parametrize("filename,expected_content", RAW_FILES.items())
def test_raw_csv_files_present_and_correct(filename, expected_content):
    """Each raw CSV must exist and contain the exact expected text."""
    path = os.path.join(RAW_DIR, filename)
    assert os.path.isfile(
        path
    ), f"Raw CSV {path} does not exist."
    with open(path, "r", encoding="utf-8") as fh:
        actual = fh.read()
    assert (
        actual == expected_content
    ), f"Contents of {path} do not match the expected initial state."


def test_processed_directory_is_empty():
    """The processed directory should exist but contain no files yet."""
    items = os.listdir(PROCESSED_DIR)
    assert (
        len(items) == 0
    ), f"Expected {PROCESSED_DIR} to be empty at the start, found: {items}"


def test_process_script_exists_and_is_faulty_template():
    """The initial process_data.sh must match the provided faulty template."""
    assert os.path.isfile(
        SCRIPT_PATH
    ), f"Required script missing: {SCRIPT_PATH}"

    # Must be executable
    st = os.stat(SCRIPT_PATH)
    assert st.st_mode & stat.S_IXUSR, f"{SCRIPT_PATH} is not executable."

    with open(SCRIPT_PATH, "r", encoding="utf-8") as fh:
        script_text = fh.read()

    # Shebang
    assert script_text.startswith(
        "#!/bin/bash"
    ), f"{SCRIPT_PATH} must start with #!/bin/bash"

    # The faulty behaviour: simple cat of all raw CSVs
    expected_line = "cat /home/user/data/raw/*.csv > /home/user/data/processed/all_sales_2023.csv"
    assert (
        expected_line in script_text
    ), f"{SCRIPT_PATH} should contain the faulty concatenation line:\n{expected_line}"

    # Should **not** yet contain 'parallel'
    assert "parallel" not in script_text, (
        f"{SCRIPT_PATH} unexpectedly contains the word 'parallel'; "
        "this should only appear *after* the student fixes the script."
    )

    # Should contain the dummy echo line
    assert 'echo "done"' in script_text, (
        f"{SCRIPT_PATH} should contain the placeholder echo command."
    )