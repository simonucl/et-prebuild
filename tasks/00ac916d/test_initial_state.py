# test_initial_state.py
#
# Pytest suite that validates the filesystem **before** the student runs any
# commands for the “log-directory size” exercise.
#
# The tests make sure that the expected directories and files exist with the
# exact byte-sizes described in the task.  We purposely do *not* check for the
# presence (or absence) of /home/user/logs_size_report.txt or any other
# artefacts the student is supposed to create later.

import os
import stat
import pytest

# Absolute paths that must exist before the learner starts working.
ROOT_DIR          = "/home/user"
APP_DIR           = "/home/user/app"
LOGS_DIR          = "/home/user/app/logs"
ERROR_LOG         = "/home/user/app/logs/error.log"
ACCESS_LOG        = "/home/user/app/logs/access.log"

# Expected byte-sizes for the two initial log files.
EXPECTED_SIZES = {
    ERROR_LOG:  2048,
    ACCESS_LOG: 3072,
}


@pytest.mark.parametrize(
    "path_to_check",
    [ROOT_DIR, APP_DIR, LOGS_DIR],
)
def test_directories_exist(path_to_check):
    """
    Assert that the mandatory directories exist and are actually directories.
    """
    assert os.path.exists(path_to_check), f"Required directory {path_to_check!r} is missing."
    assert os.path.isdir(path_to_check), f"{path_to_check!r} exists but is not a directory."


@pytest.mark.parametrize(
    "file_path",
    [ERROR_LOG, ACCESS_LOG],
)
def test_log_files_exist(file_path):
    """
    Each required log file must exist and be a regular file.
    """
    assert os.path.exists(file_path), f"Required log file {file_path!r} is missing."
    assert os.path.isfile(file_path), f"{file_path!r} exists but is not a regular file."


@pytest.mark.parametrize(
    ("file_path", "expected_size"),
    EXPECTED_SIZES.items(),
)
def test_log_file_sizes(file_path, expected_size):
    """
    The two initial log files must have the exact byte-sizes specified by the task.
    """
    actual_size = os.path.getsize(file_path)
    assert actual_size == expected_size, (
        f"{file_path!r} has size {actual_size} bytes, "
        f"but {expected_size} bytes were expected."
    )