# test_initial_state.py
#
# This pytest suite verifies that the operating-system / filesystem
# is in the expected *initial* state before the student performs any
# actions for the “log-archiving” exercise.
#
# Truth assumptions for the initial state (must already be true):
#   1.  /home/user/sample_logs/ exists.
#   2.  It contains *exactly* three files:
#          log1.log, log2.log, log3.log
#   3.  Each of those files is exactly 1 048 576 bytes (1 MiB).
#   4.  No directory named /home/user/archive/ exists yet.
#   5.  No archive or report files from the final state exist yet.
#
# If any of these assertions fail, the test harness has not provisioned
# the sandbox correctly and the student should **not** start the task.

import os
import stat
import pytest

SAMPLE_DIR = "/home/user/sample_logs"
ARCHIVE_DIR = "/home/user/archive"
EXPECTED_LOG_FILES = ("log1.log", "log2.log", "log3.log")
EXPECTED_FILE_SIZE = 1_048_576  # bytes (1 MiB)


def _full(path: str) -> str:
    "Return an absolute path inside SAMPLE_DIR."
    return os.path.join(SAMPLE_DIR, path)


def test_sample_logs_directory_exists_and_is_directory():
    assert os.path.exists(SAMPLE_DIR), (
        f"Expected directory '{SAMPLE_DIR}' to exist, but it is missing."
    )
    assert os.path.isdir(SAMPLE_DIR), (
        f"Path '{SAMPLE_DIR}' exists but is not a directory."
    )


def test_sample_logs_contains_exactly_three_expected_files():
    assert os.path.isdir(SAMPLE_DIR), "Pre-condition failed: sample_logs directory missing."

    actual_entries = sorted(os.listdir(SAMPLE_DIR))
    expected_entries = sorted(EXPECTED_LOG_FILES)

    # Check for missing or unexpected entries
    missing = set(expected_entries) - set(actual_entries)
    extra = set(actual_entries) - set(expected_entries)

    assert not missing, (
        f"The following expected log file(s) are missing in '{SAMPLE_DIR}': {', '.join(sorted(missing))}"
    )
    assert not extra, (
        f"Found unexpected file(s)/directory(ies) in '{SAMPLE_DIR}': {', '.join(sorted(extra))}. "
        f"Directory must contain only {', '.join(expected_entries)}."
    )

    # Ensure each expected entry is a *regular* file (not dir, not symlink)
    for fname in EXPECTED_LOG_FILES:
        fpath = _full(fname)
        assert os.path.isfile(fpath), f"Expected '{fpath}' to be a regular file."
        # Guard against special files (symlinks, sockets, etc.)
        mode = os.stat(fpath).st_mode
        assert stat.S_ISREG(mode), f"'{fpath}' is not a regular file."


@pytest.mark.parametrize("filename", EXPECTED_LOG_FILES)
def test_each_log_file_is_exactly_one_mebibyte(filename):
    fpath = _full(filename)
    size = os.path.getsize(fpath)
    assert size == EXPECTED_FILE_SIZE, (
        f"File '{fpath}' should be exactly {EXPECTED_FILE_SIZE} bytes "
        f"but is {size} bytes."
    )


def test_archive_directory_does_not_yet_exist():
    assert not os.path.exists(ARCHIVE_DIR), (
        f"Directory '{ARCHIVE_DIR}' should NOT exist in the initial state, "
        f"but it was found."
    )


@pytest.mark.parametrize(
    "path",
    [
        "/home/user/archive/logs_20240614.tar.gz",
        "/home/user/archive/log_archive_report.txt",
    ],
)
def test_final_state_files_do_not_exist_yet(path):
    assert not os.path.exists(path), (
        f"File '{path}' should NOT be present before the student runs their solution."
    )