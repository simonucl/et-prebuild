# test_initial_state.py
#
# Pytest suite that validates the *starting* filesystem state
# before the student performs any actions described in the
# assignment.  If any of these tests fail it means the
# environment is not prepared as the spec promises.

import os
import pytest

HOME = "/home/user"
PROJECT_DIR = os.path.join(HOME, "project")
LOG_DIR = os.path.join(PROJECT_DIR, "logs")

# ---------------------------------------------------------------------------
# Helper data describing the exact files and their expected contents
# ---------------------------------------------------------------------------

EXPECTED_FILES = {
    os.path.join(LOG_DIR, "app_2024-05-08.log"): (
        "INFO bootstrap\n"
        "WARN deprecated\n"
        "ERROR panic\n"
    ),
    os.path.join(LOG_DIR, "app_2024-05-09.log"): (
        "INFO foo\n"
        "INFO bar\n"
    ),
    os.path.join(LOG_DIR, "app_2024-05-10.log"): (
        "INFO Server started\n"
        "WARN Low memory\n"
        "INFO Connection established\n"
        "ERROR Failed to save data\n"
        "INFO Request processed\n"
    ),
    os.path.join(LOG_DIR, "app_2024-05-11.log"): (
        "INFO Task queued\n"
        "INFO Worker started\n"
        "WARN Disk space\n"
        "WARN Disk space\n"
        "ERROR Crash\n"
        "ERROR Crash\n"
        "INFO Recovered\n"
    ),
    os.path.join(LOG_DIR, "app_2024-05-12.log"): (
        "INFO Ping\n"
        "INFO Pong\n"
    ),
}

ARCHIVE_DIR = os.path.join(LOG_DIR, "archive")
SUMMARY_CSV = os.path.join(
    LOG_DIR, "summary_2024-05-10_to_2024-05-12.csv"
)
ACTION_LOG = os.path.join(LOG_DIR, "action.log")


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_project_directory_exists():
    assert os.path.isdir(PROJECT_DIR), (
        f"Expected directory {PROJECT_DIR} to exist."
    )


def test_logs_directory_exists():
    assert os.path.isdir(LOG_DIR), (
        f"Expected directory {LOG_DIR} to exist."
    )


@pytest.mark.parametrize("path", list(EXPECTED_FILES.keys()))
def test_each_log_file_exists(path):
    assert os.path.isfile(path), (
        f"Expected log file {path} to exist."
    )


@pytest.mark.parametrize(
    ("path", "expected_content"),
    list(EXPECTED_FILES.items())
)
def test_log_file_contents_exact(path, expected_content):
    """
    Verify that every provided log file has exactly the expected
    byte-for-byte content.  This guarantees deterministic counts later.
    """
    with open(path, "r", encoding="utf-8") as fp:
        actual = fp.read()
    assert actual == expected_content, (
        f"Contents of {path} differ from the specification.\n"
        f"--- expected ({len(expected_content)} bytes)\n"
        f"{expected_content!r}\n"
        f"---   actual ({len(actual)} bytes)\n"
        f"{actual!r}"
    )


def test_archive_directory_absent_initially():
    """
    Before the student runs their solution, the archive directory
    must NOT exist according to the starting situation.
    """
    assert not os.path.exists(ARCHIVE_DIR), (
        f"Directory {ARCHIVE_DIR} should NOT exist yet."
    )


def test_summary_csv_absent_initially():
    """
    The CSV summary file is supposed to be created by the student's
    script, therefore it must not be present at the start.
    """
    assert not os.path.exists(SUMMARY_CSV), (
        f"File {SUMMARY_CSV} should NOT exist before the solution runs."
    )


def test_action_log_absent_initially():
    """
    The operational log must also be absent in the pristine state.
    """
    assert not os.path.exists(ACTION_LOG), (
        f"File {ACTION_LOG} should NOT exist before the solution runs."
    )