# test_initial_state.py
#
# Pytest suite that validates the initial state of the workstation **before**
# the student starts working on the task.
#
# It checks:
#   1. Presence and permissions of /home/user/logs           (directory)
#   2. Presence, permissions, and exact byte-content of
#        /home/user/logs/system_events.csv                   (file)
#   3. That no additional files are pre-existing inside /home/user/logs
#
# NOTE:  The required *output* artifact (/home/user/logs/event_report.tsv)
#        is intentionally **NOT** tested here, because it must not exist yet.

import os
import stat
import pytest

LOG_DIR = "/home/user/logs"
CSV_PATH = os.path.join(LOG_DIR, "system_events.csv")

EXPECTED_CSV_BYTES = (
    b"timestamp,event,user,code\n"
    b"2023-03-10 12:01:05,LOGIN_SUCCESS,alice,200\n"
    b"2023-03-10 12:05:00,LOGIN_FAILURE,bob,403\n"
    b"2023-03-10 12:10:15,FILE_UPLOAD,charlie,201\n"
    b"2023-03-10 12:12:47,LOGIN_SUCCESS,dave,200\n"
    b"2023-03-10 12:15:30,FILE_DELETE,alice,204\n"
)


def _mode(path: str) -> int:
    """
    Return the permission bits (e.g. 0o755) for the given path.
    """
    return stat.S_IMODE(os.lstat(path).st_mode)


@pytest.mark.parametrize(
    "path, expected_mode",
    [
        (LOG_DIR, 0o755),
        (CSV_PATH, 0o644),
    ],
)
def test_paths_exist_with_correct_permissions(path, expected_mode):
    """
    Ensure each required path exists with the exact permissions specified
    by the task description.
    """
    assert os.path.exists(
        path
    ), f"Required path is missing: {path!r}"

    if os.path.isdir(path):
        assert _mode(path) == expected_mode, (
            f"Directory {path!r} exists but has permissions "
            f"{oct(_mode(path))}; expected {oct(expected_mode)}"
        )
    else:
        # Must be a regular file.
        assert os.path.isfile(
            path
        ), f"Expected {path!r} to be a regular file."
        assert _mode(path) == expected_mode, (
            f"File {path!r} exists but has permissions "
            f"{oct(_mode(path))}; expected {oct(expected_mode)}"
        )


def test_no_extra_files_in_logs_directory():
    """
    Only 'system_events.csv' should be present initially inside /home/user/logs.
    Hidden files (dot-files) are not expected per the specification.
    """
    contents = os.listdir(LOG_DIR)
    assert contents == [
        "system_events.csv"
    ], (
        f"Unexpected files found in {LOG_DIR!r}: {contents!r}. "
        "Only 'system_events.csv' should exist at this stage."
    )


def test_system_events_csv_exact_content():
    """
    The CSV must match the exact bytes given in the task description,
    including newlines.
    """
    with open(CSV_PATH, "rb") as fh:
        data = fh.read()

    assert (
        data == EXPECTED_CSV_BYTES
    ), (
        f"The contents of {CSV_PATH!r} do not match the expected "
        "initial data set.\n\n"
        "Expected bytes:\n"
        f"{EXPECTED_CSV_BYTES!r}\n\n"
        "Actual bytes:\n"
        f"{data!r}"
    )