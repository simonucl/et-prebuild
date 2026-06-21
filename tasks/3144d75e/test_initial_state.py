# test_initial_state.py
#
# This test-suite validates the state of the filesystem *before* the student
# starts working on the task.  It checks only the artefacts that must already
# exist, i.e. the directory /home/user/release-logs/raw/ and the two raw log
# files inside it.  It explicitly does **not** look for any of the output files
# that the student is expected to create later.

import pathlib
import pytest

HOME = pathlib.Path("/home/user")
RELEASE_LOGS_DIR = HOME / "release-logs"
RAW_DIR = RELEASE_LOGS_DIR / "raw"
APP1_LOG = RAW_DIR / "app1.log"
APP2_LOG = RAW_DIR / "app2.log"


@pytest.mark.describe("Verify required directories exist")
def test_directories_exist():
    assert RELEASE_LOGS_DIR.is_dir(), (
        f"Missing directory: {RELEASE_LOGS_DIR}. "
        "The directory /home/user/release-logs/ must exist."
    )
    assert RAW_DIR.is_dir(), (
        f"Missing directory: {RAW_DIR}. "
        "The directory /home/user/release-logs/raw/ must exist."
    )


@pytest.mark.describe("Verify required raw log files exist")
@pytest.mark.parametrize(
    "log_path",
    [APP1_LOG, APP2_LOG],
)
def test_raw_log_files_exist(log_path):
    assert log_path.is_file(), (
        f"Missing file: {log_path}. "
        "Both raw log files must already be present before the task begins."
    )


# Expected content for the two raw logs -------------------------------------- #

APP1_EXPECTED_LINES = [
    "2023-12-01 08:15:42,123 INFO User 192.168.1.10 logged in",
    "2023-12-01 08:16:12,456 ERROR Failed to load resource /api/data",
    "2023-12-01 08:17:05,789 WARN Cache miss for user 42",
    "2023-12-01 09:03:22,105 ERROR Database timeout after 30s",
    "2023-12-01 09:05:01,333 INFO User 192.168.1.15 logged out",
]

APP2_EXPECTED_LINES = [
    "2023-12-01 08:20:11,111 INFO Deployment started by user devops",
    "2023-12-01 08:21:45,222 ERROR Service xyz failed health-check",
    "2023-12-01 08:23:30,555 INFO Service xyz restarted successfully",
    "2023-12-01 08:24:18,777 ERROR Could not connect to redis at 10.0.0.5:6379",
    "2023-12-01 08:25:55,999 INFO Deployment finished in 344s",
]


@pytest.mark.describe("Verify exact content of /home/user/release-logs/raw/app1.log")
def test_app1_log_content():
    with APP1_LOG.open("r", encoding="utf-8") as fh:
        actual_lines = fh.read().splitlines()
    assert actual_lines == APP1_EXPECTED_LINES, (
        "The content of app1.log does not match the expected initial state.\n"
        f"Expected ({len(APP1_EXPECTED_LINES)} lines):\n"
        + "\n".join(APP1_EXPECTED_LINES)
        + "\n\n"
        f"Actual ({len(actual_lines)} lines):\n"
        + "\n".join(actual_lines)
    )


@pytest.mark.describe("Verify exact content of /home/user/release-logs/raw/app2.log")
def test_app2_log_content():
    with APP2_LOG.open("r", encoding="utf-8") as fh:
        actual_lines = fh.read().splitlines()
    assert actual_lines == APP2_EXPECTED_LINES, (
        "The content of app2.log does not match the expected initial state.\n"
        f"Expected ({len(APP2_EXPECTED_LINES)} lines):\n"
        + "\n".join(APP2_EXPECTED_LINES)
        + "\n\n"
        f"Actual ({len(actual_lines)} lines):\n"
        + "\n".join(actual_lines)
    )