# test_initial_state.py
#
# This pytest suite validates the filesystem _before_ the student
# performs any action.  It asserts that
#   1) /home/user/build-logs/ exists and is a directory.
#   2) /home/user/build-logs/release_2023-05-18.log exists and its
#      content exactly matches the truth data supplied in the task
#      description (including all spaces and trailing newline).
#
# NOTE: Per the grading-framework rules we intentionally DO NOT look
#       for the yet-to-be-created output file
#       /home/user/build-logs/release_2023-05-18-deploy-errors.log.

import os
import pytest

BUILD_LOG_DIR = "/home/user/build-logs"
RELEASE_LOG = os.path.join(BUILD_LOG_DIR, "release_2023-05-18.log")


def test_build_log_directory_exists_and_is_dir():
    assert os.path.exists(
        BUILD_LOG_DIR
    ), f"Required directory {BUILD_LOG_DIR!r} is missing."
    assert os.path.isdir(
        BUILD_LOG_DIR
    ), f"Path {BUILD_LOG_DIR!r} exists but is not a directory."


def test_release_log_file_exists():
    assert os.path.isfile(
        RELEASE_LOG
    ), f"Required log file {RELEASE_LOG!r} is missing."


def test_release_log_content_is_exact():
    expected_content = (
        "[2023-05-18 14:22:01] [INFO]  [compile] Compilation successful\n"
        "[2023-05-18 14:22:05] [WARN]  [test]    Unit test took longer than expected\n"
        "[2023-05-18 14:22:10] [ERROR] [compile] Missing semicolon in source/foo.c\n"
        "[2023-05-18 14:22:15] [INFO]  [package] Packaging artifacts\n"
        "[2023-05-18 14:22:20] [ERROR] [deploy]  Cannot connect to production server\n"
        "[2023-05-18 14:22:25] [INFO]  [deploy]  Connection re-established\n"
        "[2023-05-18 14:22:30] [ERROR] [deploy]  Deployment aborted due to previous errors\n"
        "[2023-05-18 14:22:35] [INFO]  [cleanup] Temporary files removed\n"
        "[2023-05-18 14:22:40] [WARN]  [deploy]  Retrying deployment\n"
        "[2023-05-18 14:22:45] [ERROR] [deploy]  Retry failed, manual intervention required\n"
    )

    with open(RELEASE_LOG, "r", encoding="utf-8") as fh:
        actual_content = fh.read()

    assert (
        actual_content == expected_content
    ), "Content of release_2023-05-18.log does not match the expected truth data."