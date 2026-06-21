# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem/OS state
# before the student creates anything.  It must be run **before**
# the student starts working on the assignment.

import os
from pathlib import Path

LOG_DIR = Path("/home/user/logs")
LOG_FILE = LOG_DIR / "app_2023-08-15.log"
SCRIPTS_DIR = Path("/home/user/scripts")
FILTER_SCRIPT = SCRIPTS_DIR / "filter_errors.sh"
OUTPUT_DIR = Path("/home/user/output")
RUN_LOG = Path("/home/user/filter_run.log")

EXPECTED_LOG_LINES = [
    "[2023-08-15 09:15:23] INFO User 123 logged in\n",
    "[2023-08-15 09:15:24] DEBUG Cache miss for key 'profile_123'\n",
    "[2023-08-15 09:15:25] ERROR Payment failed for order 987: insufficient_funds\n",
    "[2023-08-15 09:15:26] WARN Slow query detected (850ms) on endpoint /api/items\n",
    "[2023-08-15 09:15:27] INFO HTTP/1.1 200 OK\n",
    "[2023-08-15 09:15:28] ERROR HTTP/1.1 500 Internal Server Error\n",
    "[2023-08-15 09:15:29] FATAL OutOfMemoryError: Java heap space\n",
    "[2023-08-15 09:15:30] INFO User 456 logged out\n",
    "[2023-08-15 09:15:31] ERROR Payment failed for order 988: card_expired\n",
]
EXPECTED_LOG_CONTENT = "".join(EXPECTED_LOG_LINES)


def test_logs_directory_exists():
    assert LOG_DIR.is_dir(), f"Required directory missing: {LOG_DIR}"


def test_log_file_exists():
    assert LOG_FILE.is_file(), f"Required log file missing: {LOG_FILE}"


def test_log_file_contents_exact():
    """
    The log file must contain exactly the nine lines provided in the specification,
    each ending with a single newline.  Byte-for-byte equality is required.
    """
    actual = LOG_FILE.read_text(encoding="utf-8")
    assert actual == EXPECTED_LOG_CONTENT, (
        f"{LOG_FILE} does not match the expected contents.\n"
        "If you have already modified this file, revert it before starting the task."
    )


def test_filter_script_absent_initially():
    """
    The developer has not yet created filter_errors.sh, so it must NOT exist
    at the beginning of the exercise.
    """
    assert not FILTER_SCRIPT.exists(), (
        f"{FILTER_SCRIPT} unexpectedly exists. "
        "The assignment requires you to create this script during your solution."
    )


def test_output_dir_absent_initially():
    """
    The output directory should not exist before the script is executed
    for the first time.
    """
    assert not OUTPUT_DIR.exists(), (
        f"{OUTPUT_DIR} already exists. Remove it before starting the task."
    )


def test_run_log_absent_initially():
    """
    The run log is produced by the yet-to-be-written script; it must not
    exist at the start.
    """
    assert not RUN_LOG.exists(), (
        f"{RUN_LOG} already exists. It should be created only by the script."
    )