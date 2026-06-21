# test_initial_state.py
#
# This pytest module validates the machine *before* the student starts
# working on the task.  It checks that the raw input file is present with
# exactly the expected content and that the output directory does **not**
# yet exist.

import os
import stat
import pytest

HOME = "/home/user"
DATASETS_DIR = os.path.join(HOME, "datasets")
RAW_LOG_PATH = os.path.join(DATASETS_DIR, "raw_records.log")
CLEAN_DIR = os.path.join(HOME, "clean_data")

# --------------------------------------------------------------------------- #
# Expected data for /home/user/datasets/raw_records.log
# --------------------------------------------------------------------------- #
EXPECTED_LINES = [
    "ABC123 SUCCESS Data loaded",
    "DEF456 FAILURE Data missing",
    "XYZ789 SUCCESS Completed",
    "abc111 SUCCESS lowercase",
    "123ABC SUCCESS misplaced",
    "LMN000 SUCCESS component",
    "NOP999 FAULT unexpected",
    "QRS321 SUCCESS processed",
    "TUV654 DEFER waiting",
    "GHI777 SUCCESS final",
]

EXPECTED_CONTENT = "\n".join(EXPECTED_LINES) + "\n"  # each line must end with LF


# --------------------------------------------------------------------------- #
# Utility helpers
# --------------------------------------------------------------------------- #
def _read_file(path):
    with open(path, "rb") as fh:
        return fh.read()


def _is_executable(mode):
    """Return True if user has execute bit set (for directories)."""
    return bool(mode & stat.S_IXUSR)


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_datasets_directory_exists_and_is_accessible():
    assert os.path.isdir(
        DATASETS_DIR
    ), f"Required directory {DATASETS_DIR!r} is missing or is not a directory."
    st = os.stat(DATASETS_DIR)
    assert _is_executable(
        st.st_mode
    ), f"Directory {DATASETS_DIR!r} is not accessible (execute bit not set for user)."


def test_raw_log_file_exists_with_expected_content():
    assert os.path.isfile(
        RAW_LOG_PATH
    ), f"Required file {RAW_LOG_PATH!r} does not exist."

    content = _read_file(RAW_LOG_PATH)
    try:
        decoded = content.decode("utf-8")
    except UnicodeDecodeError as err:
        pytest.fail(
            f"File {RAW_LOG_PATH!r} is not valid UTF-8: {err}"
        )

    assert (
        decoded == EXPECTED_CONTENT
    ), (
        f"Content of {RAW_LOG_PATH!r} does not match the expected initial data.\n"
        "If the file was modified, restore it to exactly the required state."
    )

    # Extra sanity: verify that there are exactly 10 lines, each ending with LF
    raw_lines = decoded.splitlines(keepends=True)
    assert len(raw_lines) == 10, (
        f"{RAW_LOG_PATH!r} should contain exactly 10 lines (found {len(raw_lines)})."
    )
    for idx, line in enumerate(raw_lines, 1):
        assert line.endswith(
            "\n"
        ), f"Line {idx} in {RAW_LOG_PATH!r} is missing the trailing LF newline."


def test_clean_data_directory_does_not_exist_yet():
    assert not os.path.exists(
        CLEAN_DIR
    ), (
        f"Directory {CLEAN_DIR!r} should NOT exist before the student runs "
        "their solution.  Please remove or rename it so the task starts from a clean state."
    )