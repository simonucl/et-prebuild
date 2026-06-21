# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem
# state required for the “filtered build log” task.  These tests must pass
# *before* the student performs any actions.  If they fail, the student is
# missing prerequisite files or directories.
#
# Rules verified:
#   1. The directory /home/user/build_logs/ exists and is writable.
#   2. The file   /home/user/build_logs/build.log  exists.
#   3. build.log contains exactly the expected seven lines (no more, no less,
#      and in the correct order).
#
# NOTE: Per the grading-spec rules, we deliberately do *not* test for the
#       presence (or absence) of any output files such as
#       /home/user/build_logs/uploaded_jars.log.

import os
import stat
import pytest

# Full, absolute paths used throughout (per rubric).
BUILD_LOG_DIR = "/home/user/build_logs"
BUILD_LOG_FILE = os.path.join(BUILD_LOG_DIR, "build.log")

EXPECTED_BUILD_LOG_LINES = [
    "[2023-07-14 10:23:45] INFO Uploaded artifact: commons-lang3-3.12.0.jar (size 290381 bytes)",
    "[2023-07-14 10:23:46] INFO Uploaded artifact: myapp-1.0.0.tar.gz (size 1839201 bytes)",
    "[2023-07-14 10:23:47] WARN Skipped artifact: guava-31.0.1.jar - already exists",
    "[2023-07-14 10:23:48] INFO Uploaded artifact: guava-31.0.1.jar (size 2798096 bytes)",
    "[2023-07-14 10:23:49] ERROR Failed to upload artifact: invalid-file.txt",
    "some unrelated line",
    "[2023-07-14 10:23:50] INFO Uploaded artifact: junit-4.13.2.jar (size 238947 bytes)",
]


def test_build_log_directory_exists_and_writable():
    """
    The directory /home/user/build_logs/ must exist, be a directory, and be
    writable by the current user.  These are prerequisites for the task.
    """
    assert os.path.exists(
        BUILD_LOG_DIR
    ), f"Required directory {BUILD_LOG_DIR!r} does not exist."
    assert os.path.isdir(
        BUILD_LOG_DIR
    ), f"Expected {BUILD_LOG_DIR!r} to be a directory, but it is not."

    # Check write permission for the current user.
    is_writable = os.access(BUILD_LOG_DIR, os.W_OK)
    assert (
        is_writable
    ), f"Directory {BUILD_LOG_DIR!r} is not writable by the current user."


def test_build_log_file_exists():
    """
    The file build.log must be present inside /home/user/build_logs/.
    """
    assert os.path.isfile(
        BUILD_LOG_FILE
    ), f"Required log file {BUILD_LOG_FILE!r} is missing."


def test_build_log_contents_exact_match():
    """
    The build.log file must contain exactly the seven expected lines, in order.
    Extra or missing lines will cause this test to fail with a clear diff.
    """
    with open(BUILD_LOG_FILE, "r", encoding="utf-8") as fp:
        actual_lines = fp.read().splitlines()  # removes trailing newlines

    assert (
        actual_lines == EXPECTED_BUILD_LOG_LINES
    ), (
        "Contents of build.log do not match the expected initial state.\n"
        "Expected lines:\n"
        + "\n".join(EXPECTED_BUILD_LOG_LINES)
        + "\n\nActual lines:\n"
        + "\n".join(actual_lines)
    )