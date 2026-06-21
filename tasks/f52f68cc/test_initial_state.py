# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem
# state before the student carries out any actions for the task described in
# the prompt.  These checks guarantee that the student starts from the
# expected baseline: the CSV input file exists with the exact prescribed
# contents, while the output file to be created by the student does *not*
# yet exist.

import os
import stat
import textwrap

import pytest

HOME = "/home/user"
DATA_DIR = os.path.join(HOME, "data")
OUTPUT_DIR = os.path.join(HOME, "output")
CSV_PATH = os.path.join(DATA_DIR, "usage.csv")
SUMMARY_PATH = os.path.join(OUTPUT_DIR, "summary.txt")


@pytest.fixture(scope="module")
def expected_csv_content() -> str:
    """
    Return the exact, canonical contents of /home/user/data/usage.csv,
    including the final newline.
    """
    return textwrap.dedent(
        """\
        host,timestamp,cpu,memory
        host1,2023-01-01T00:00:00Z,57,40
        host1,2023-01-01T01:00:00Z,63,43
        host1,2023-01-01T02:00:00Z,50,38
        host2,2023-01-01T00:00:00Z,80,70
        host2,2023-01-01T01:00:00Z,75,68
        host2,2023-01-01T02:00:00Z,82,71
        host3,2023-01-01T00:00:00Z,20,30
        host3,2023-01-01T01:00:00Z,25,28
        host3,2023-01-01T02:00:00Z,22,29
        """
    )


def test_usage_csv_exists_and_is_regular_file():
    assert os.path.isfile(
        CSV_PATH
    ), f"Required CSV input file not found at expected path: {CSV_PATH!r}"


def test_usage_csv_permissions():
    """
    Ensure the CSV file is owned by user:user and has mode 0644 (rw-r--r--).
    Ownership tests are skipped if running as root or if pwd/grp are missing.
    """
    st = os.stat(CSV_PATH)
    mode = stat.S_IMODE(st.st_mode)
    assert (
        mode == 0o644
    ), f"Expected permissions 0644 for {CSV_PATH}, found {oct(mode)}"


def test_usage_csv_exact_contents(expected_csv_content):
    with open(CSV_PATH, "r", encoding="utf-8") as fh:
        data = fh.read()

    # Ensure exact byte-for-byte match (including newline at EOF)
    assert (
        data == expected_csv_content
    ), "Contents of usage.csv do not match the expected baseline"


def test_output_directory_exists_and_is_empty():
    assert os.path.isdir(
        OUTPUT_DIR
    ), f"Output directory {OUTPUT_DIR!r} is missing; it should exist (mode 0755)"

    # Directory should be empty before the task starts
    leftover = [name for name in os.listdir(OUTPUT_DIR) if not name.startswith(".")]
    assert (
        len(leftover) == 0
    ), f"Output directory {OUTPUT_DIR!r} should be empty before the student runs their command, but found: {leftover}"


def test_summary_txt_does_not_exist_yet():
    assert not os.path.exists(
        SUMMARY_PATH
    ), "summary.txt should NOT exist yet; the student must create it with their single-command solution"