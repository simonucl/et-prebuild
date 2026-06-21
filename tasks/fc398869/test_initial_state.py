# test_initial_state.py
#
# This pytest suite validates that the starting filesystem state is
# exactly as expected *before* the student performs any actions.
#
# It verifies:
#   • The three original *.log files exist with the exact expected content.
#   • None of the files that the student is supposed to create yet exist
#     (error_report.txt, error_summary.log, logs_backup.tar.gz).
#
# NOTE: All paths are absolute and point into /home/user.

import os
import gzip
import tarfile
import pytest

BASE_DIR = "/home/user/logs"

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def read_lines(path):
    """Read a text file and return the list of lines **without** trailing newlines."""
    with open(path, encoding="utf-8") as fp:
        return [line.rstrip("\n") for line in fp.readlines()]

# ---------------------------------------------------------------------------
# Expected data for the original log files
# ---------------------------------------------------------------------------

EXPECTED_LOGS = {
    os.path.join(BASE_DIR, "app1", "server.log"): [
        "[2023-08-10 10:00:01] INFO  Server started",
        "[2023-08-10 10:05:11] ERROR Failed to connect to DB",
        "[2023-08-10 10:06:43] WARN  Low disk space",
        "[2023-08-10 10:07:02] ERROR User authentication failed",
    ],
    os.path.join(BASE_DIR, "app1", "access.log"): [
        '127.0.0.1 - - [10/Aug/2023:10:01:00 +0000] "GET /index.html HTTP/1.1" 200 1024',
        '127.0.0.1 - - [10/Aug/2023:10:06:00 +0000] "POST /login HTTP/1.1" 500 2048 ERROR Internal server error',
    ],
    os.path.join(BASE_DIR, "app2", "backend.log"): [
        "2023-08-10 10:10:00,001 INFO  Job started",
        "2023-08-10 10:12:22,333 ERROR NullPointer at worker.go:88",
        "2023-08-10 10:13:30,555 INFO  Job finished",
    ],
}

# Files that must **NOT** exist yet.
PROHIBITED_ARTIFACTS = [
    os.path.join(BASE_DIR, "error_report.txt"),
    os.path.join(BASE_DIR, "error_summary.log"),
    os.path.join(BASE_DIR, "archive", "logs_backup.tar.gz"),
]

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("path,expected_lines", list(EXPECTED_LOGS.items()))
def test_original_log_files_exist_with_expected_content(path, expected_lines):
    # 1. The file must exist.
    assert os.path.isfile(
        path
    ), f"Expected original log file not found: {path}"

    # 2. The content must match exactly, line-for-line.
    actual_lines = read_lines(path)
    assert (
        actual_lines == expected_lines
    ), (
        f"Content mismatch in {path}.\n"
        f"Expected lines:\n{expected_lines!r}\n\n"
        f"Actual lines:\n{actual_lines!r}"
    )


def test_base_directory_structure():
    """
    Ensure the directory /home/user/logs exists and contains at least the
    sub-directories `app1` and `app2`.
    """
    assert os.path.isdir(
        BASE_DIR
    ), f"Base directory {BASE_DIR} does not exist."

    for sub in ("app1", "app2"):
        subdir = os.path.join(BASE_DIR, sub)
        assert os.path.isdir(
            subdir
        ), f"Expected sub-directory missing: {subdir}"


@pytest.mark.parametrize("artifact", PROHIBITED_ARTIFACTS)
def test_artifacts_do_not_exist_yet(artifact):
    """
    Verify that none of the files the student is supposed to create
    already exist.
    """
    assert not os.path.exists(
        artifact
    ), f"File {artifact} should NOT exist before the task is attempted."


def test_no_archive_tarball_yet():
    """
    If the archive directory does happen to exist for some reason,
    ensure it does *not* yet contain a tarball. This guards against a
    half-completed previous run.
    """
    archive_dir = os.path.join(BASE_DIR, "archive")
    if os.path.isdir(archive_dir):
        tarball = os.path.join(archive_dir, "logs_backup.tar.gz")
        assert not os.path.exists(
            tarball
        ), "logs_backup.tar.gz should not exist yet."