# test_initial_state.py
#
# Pytest suite that verifies the initial state of the OS / filesystem
# BEFORE the student performs any action for the “hostname look-ups”
# exercise.
#
# The tests check only the pre-existing resources and do **not**
# reference any of the output directories or files that the learner
# is expected to create (/home/user/qa_dns, etc.).

import os
from pathlib import Path

QA_ENV_DIR = Path("/home/user/qa_env")
TEST_HOSTS_FILE = QA_ENV_DIR / "test_hosts"

# The exact, byte-for-byte content the seed hosts-like file must have.
EXPECTED_TEST_HOSTS_CONTENT = (
    "10.10.0.5    api.dev.local api\n"
    "10.10.0.6    db.dev.local db\n"
    "10.10.0.7    cache.dev.local cache\n"
    "\n"
    "# An extra test entry that should be ignored by the agent\n"
    "# 10.10.0.8    logging.dev.local log\n"
)


def test_qa_env_directory_exists():
    """The seed directory /home/user/qa_env must exist and be a directory."""
    assert QA_ENV_DIR.exists(), (
        f"Required directory {QA_ENV_DIR} does not exist. "
        "The exercise's seed files are missing."
    )
    assert QA_ENV_DIR.is_dir(), (
        f"{QA_ENV_DIR} exists but is not a directory."
    )


def test_test_hosts_file_exists():
    """The seed file /home/user/qa_env/test_hosts must exist and be a regular file."""
    assert TEST_HOSTS_FILE.exists(), (
        f"Required file {TEST_HOSTS_FILE} does not exist."
    )
    assert TEST_HOSTS_FILE.is_file(), (
        f"{TEST_HOSTS_FILE} exists but is not a regular file."
    )


def test_test_hosts_file_content_is_exact():
    """
    The contents of /home/user/qa_env/test_hosts must match the expected
    multi-line string exactly, including blanks and the trailing newline.
    """
    actual_content = TEST_HOSTS_FILE.read_text(encoding="utf-8")
    assert actual_content == EXPECTED_TEST_HOSTS_CONTENT, (
        "The contents of /home/user/qa_env/test_hosts do not match the "
        "expected seed data.\n\n"
        "----- Expected (byte-for-byte) -----\n"
        f"{EXPECTED_TEST_HOSTS_CONTENT!r}\n"
        "-----   Actual (byte-for-byte)  -----\n"
        f"{actual_content!r}\n"
        "------------------------------------"
    )