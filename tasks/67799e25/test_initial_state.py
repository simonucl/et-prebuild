# test_initial_state.py
#
# This pytest suite validates the initial state of the operating system /
# file-system before the student performs any actions for the “error-report”
# exercise.  ONLY the pre-existing artefacts are checked; output files and
# directories that the student is supposed to create are **not** tested here.

import os
import stat
import pytest

LOG_DIR = "/home/user/logs"
RELEASE_LOG = os.path.join(LOG_DIR, "release-2023-07-01.log")

# Exact file contents expected in /home/user/logs/release-2023-07-01.log
EXPECTED_LOG_CONTENT = (
    "2023-07-01 10:15:02 [INFO] Starting deployment\n"
    "2023-07-01 10:15:05 [WARN] Slow response from artifact repository\n"
    "2023-07-01 10:15:10 [ERROR] Failed to fetch artifact build-1234\n"
    "2023-07-01 10:15:12 [INFO] Retrying...\n"
    "2023-07-01 10:15:18 [ERROR] Failed to fetch artifact build-1234\n"
    "2023-07-01 10:15:30 [INFO] Deployment aborted\n"
    "2023-07-01 10:15:31 [ERROR] Rollback failed: missing snapshot\n"
    "2023-07-01 10:15:35 [INFO] Manual intervention required\n"
)


def test_logs_directory_exists():
    """The /home/user/logs directory must exist and be a directory."""
    assert os.path.isdir(LOG_DIR), (
        f"Required directory '{LOG_DIR}' is missing or not a directory."
    )


def test_release_log_file_exists_and_permissions():
    """
    The release log file must exist, be a regular file, world-readable,
    and have mode 0644 exactly (rw-r--r--).
    """
    assert os.path.isfile(RELEASE_LOG), (
        f"Required log file '{RELEASE_LOG}' is missing."
    )

    st = os.stat(RELEASE_LOG)
    file_mode = stat.S_IMODE(st.st_mode)
    expected_mode = 0o644
    assert file_mode == expected_mode, (
        f"Log file '{RELEASE_LOG}' should have mode "
        f"{oct(expected_mode)} (rw-r--r--) but is {oct(file_mode)}."
    )


def test_release_log_file_contents():
    """The contents of the log file must match the exercise specification exactly."""
    with open(RELEASE_LOG, "r", encoding="utf-8") as f:
        actual = f.read()

    assert actual == EXPECTED_LOG_CONTENT, (
        f"Contents of '{RELEASE_LOG}' do not match the expected template.\n"
        "If the file was modified or copied incorrectly, please restore it "
        "to the state described in the task instructions."
    )