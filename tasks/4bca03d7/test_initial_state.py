# test_initial_state.py
#
# This test-suite verifies that the starting filesystem state exactly matches
# what the assignment describes.  It purposely does *not* look at any of the
# artefacts the student is supposed to create later under /home/user/diagnostics.

import os
import pytest

HOME = "/home/user"
LOG_DIR = os.path.join(HOME, "logs")

# Expected contents for each input log file (no trailing newline characters).
EXPECTED_LOG_CONTENT = {
    os.path.join(LOG_DIR, "webapp1.log"): [
        "[2023-11-04 09:15:23] INFO User login id=23",
        "[2023-11-04 09:16:00] WARN Session delay",
        "[2023-11-04 09:17:10] ERROR ERR101 Failed query",
        "[2023-11-04 09:19:30] INFO Data saved",
        "[2023-11-04 09:20:05] ERROR ERR102 Timeout calling API",
    ],
    os.path.join(LOG_DIR, "webapp2.log"): [
        "[2023-11-04 09:12:00] INFO Service started",
        "[2023-11-04 09:13:34] ERROR ERR201 Missing config",
        "[2023-11-04 09:14:00] WARN Cache cold",
        "[2023-11-04 09:15:45] ERROR ERR201 Missing config",
        "[2023-11-04 09:18:50] INFO Healthcheck OK",
        "[2023-11-04 09:19:59] ERROR ERR202 Disk full",
    ],
    os.path.join(LOG_DIR, "dbservice.log"): [
        "[2023-11-04 09:10:10] INFO Connection pool created",
        "[2023-11-04 09:11:12] ERROR ERR301 Connection refused",
        "[2023-11-04 09:14:50] WARN Slow query detected",
        "[2023-11-04 09:16:30] ERROR ERR301 Connection refused",
        "[2023-11-04 09:18:00] ERROR ERR302 Deadlock found",
    ],
}


def _read_file_stripped(path):
    """Return the file lines without their trailing newlines."""
    with open(path, "r", encoding="utf-8") as fh:
        return [ln.rstrip("\n") for ln in fh.readlines()]


def test_log_directory_exists():
    assert os.path.isdir(
        LOG_DIR
    ), f"Required log directory {LOG_DIR!r} is missing."


@pytest.mark.parametrize("path, expected_lines", EXPECTED_LOG_CONTENT.items())
def test_log_file_exists_and_has_expected_content(path, expected_lines):
    # 1) File must exist
    assert os.path.isfile(
        path
    ), f"Expected log file {path!r} is missing."

    # 2) File must be readable
    assert os.access(
        path, os.R_OK
    ), f"Log file {path!r} exists but is not readable."

    # 3) File must have exactly the expected content
    actual_lines = _read_file_stripped(path)
    assert (
        actual_lines == expected_lines
    ), (
        f"Contents of {path!r} do not match the expected starting state.\n"
        f"Expected ({len(expected_lines)} lines):\n{expected_lines}\n\n"
        f"Actual   ({len(actual_lines)} lines):\n{actual_lines}"
    )