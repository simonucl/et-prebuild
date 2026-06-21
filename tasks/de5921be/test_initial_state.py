# test_initial_state.py
#
# This pytest suite validates the initial state of the operating-system
# before the student starts working on the “large log alert” task.
#
# The checks assert that:
#   • the /home/user/monitoring/logs directory exists;
#   • exactly three *.log files are present in it (access, error, debug);
#   • each file has the correct size in bytes;
#   • no other files or sub-directories are present inside /home/user/monitoring/logs;
#   • the /home/user/monitoring/alerts directory (and the CSV report) do **not** yet exist.
#
# If any assertion fails the corresponding error message will tell the
# student precisely what is missing or unexpected.

import os
import stat
import pytest

HOME = "/home/user"
LOGS_DIR = os.path.join(HOME, "monitoring", "logs")
ALERTS_DIR = os.path.join(HOME, "monitoring", "alerts")
REPORT_FILE = os.path.join(ALERTS_DIR, "large_logs_report.csv")

EXPECTED_LOG_FILES = {
    "access.log": 2_000_000,   # 2000000 bytes
    "error.log":   500_000,    #  500000 bytes
    "debug.log": 1_200_000,    # 1200000 bytes
}


def _full_path(filename: str) -> str:
    """Return the absolute path to a file inside the logs directory."""
    return os.path.join(LOGS_DIR, filename)


def test_logs_directory_exists_and_is_directory():
    assert os.path.exists(LOGS_DIR), (
        f"Required directory {LOGS_DIR!r} does not exist."
    )
    assert os.path.isdir(LOGS_DIR), (
        f"{LOGS_DIR!r} exists but is not a directory."
    )

    # Optional: check directory permissions (must at least be readable)
    mode = os.stat(LOGS_DIR).st_mode
    assert bool(mode & stat.S_IRUSR), (
        f"{LOGS_DIR!r} exists but is not readable."
    )


@pytest.mark.parametrize("filename, expected_size", EXPECTED_LOG_FILES.items())
def test_each_expected_log_file_exists_with_correct_size(filename, expected_size):
    path = _full_path(filename)
    assert os.path.exists(path), (
        f"Expected log file {path!r} is missing."
    )
    assert os.path.isfile(path), (
        f"{path!r} exists but is not a regular file."
    )

    actual_size = os.path.getsize(path)
    assert actual_size == expected_size, (
        f"{path!r} has size {actual_size} bytes; expected {expected_size} bytes."
    )


def test_no_extra_files_in_logs_directory():
    """
    The task specification states that /home/user/monitoring/logs
    'contains only *.log files'.  Ensure there are no unexpected files
    or sub-directories.
    """
    entries = os.listdir(LOGS_DIR)
    expected = set(EXPECTED_LOG_FILES.keys())
    actual = set(entries)

    # Are there missing files?
    missing = expected - actual
    assert not missing, (
        f"The following expected log files are missing from {LOGS_DIR!r}: "
        f"{', '.join(sorted(missing))}"
    )

    # Are there extra files or directories?
    extra = actual - expected
    assert not extra, (
        f"Found unexpected entries in {LOGS_DIR!r}: "
        f"{', '.join(sorted(extra))}. "
        "The directory should contain only the specified *.log files."
    )


def test_alerts_directory_and_report_do_not_yet_exist():
    """
    Before the student works on the task, the alerts directory and the
    CSV report must not exist.  The student will create them.
    """
    assert not os.path.exists(ALERTS_DIR), (
        f"{ALERTS_DIR!r} already exists. The alerts directory should "
        "be created by the student's solution."
    )

    assert not os.path.exists(REPORT_FILE), (
        f"Report file {REPORT_FILE!r} already exists. It should be "
        "generated only after the student runs their command."
    )