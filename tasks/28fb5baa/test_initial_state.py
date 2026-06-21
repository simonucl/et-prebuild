# test_initial_state.py
#
# This pytest suite validates the **initial** filesystem state that must be
# present *before* the student performs any actions.  It purposefully avoids
# checking for the output artefacts (the reports directory or its files) so
# that it only verifies the given starting conditions.

import os
from pathlib import Path

LOGS_DIR = Path("/home/user/project/logs")
APP_LOG = LOGS_DIR / "app.log"

EXPECTED_APP_LOG_CONTENT = (
    "2023-08-01 10:15:20 INFO Starting application\n"
    "2023-08-01 10:15:21 WARN Low memory\n"
    "2023-08-01 10:15:22 ERROR Could not connect to database\n"
    "2023-08-01 10:15:25 INFO Retrying connection\n"
    "2023-08-01 10:15:30 ERROR Connection timeout\n"
    "2023-08-01 10:15:45 INFO Shutdown initiated\n"
)


def test_logs_directory_exists_and_is_directory():
    """
    The directory /home/user/project/logs must exist and be a directory.
    """
    assert LOGS_DIR.exists(), (
        f"Required directory {LOGS_DIR} is missing. "
        "The initial setup should already have created it."
    )
    assert LOGS_DIR.is_dir(), (
        f"{LOGS_DIR} exists but is not a directory. "
        "Expected a directory containing the sample log file."
    )


def test_app_log_exists_and_has_expected_content():
    """
    The sample application log must exist and match the exact expected content,
    including its trailing newline.
    """
    assert APP_LOG.exists(), (
        f"Required log file {APP_LOG} is missing. "
        "The initial setup should provide this file."
    )
    assert APP_LOG.is_file(), (
        f"{APP_LOG} exists but is not a regular file. "
        "Expected a regular text log file."
    )

    # Read content and compare exactly.
    file_content = APP_LOG.read_text(encoding="utf-8")
    assert (
        file_content == EXPECTED_APP_LOG_CONTENT
    ), (
        "The content of /home/user/project/logs/app.log does not match the "
        "expected initial log content. Please ensure the file has the exact "
        "lines (including the final newline) specified in the task description."
    )