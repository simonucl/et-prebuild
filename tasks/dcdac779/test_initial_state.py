# test_initial_state.py
#
# Pytest suite that validates the filesystem *before* the student runs
# any commands.  It asserts that the required directory and source file
# exist with the exact expected contents, and that the output file has
# NOT yet been created.

from pathlib import Path

import pytest

# Paths used throughout the tests
DATA_DIR = Path("/home/user/data/users_db")
PASSWD_FILE = DATA_DIR / "passwd.txt"
SUMMARY_FILE = Path("/home/user/account_summary.log")

# The precise, line-by-line contents that must exist in passwd.txt
EXPECTED_PASSWD_CONTENT = (
    "root:x:0:0:root:/root:/bin/bash\n"
    "daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin\n"
    "alice:x:1000:1000:Alice Admin:/home/alice:/bin/bash\n"
    "bob:x:1001:1001:Bob Builder:/home/bob:/bin/zsh\n"
    "charlie:x:1002:1002:Charlie Chaplin:/home/charlie:/bin/bash\n"
    "dave:x:1003:1003:Dave Developer:/home/dave:/usr/sbin/nologin\n"
    "erin:x:1004:1004:Erin Example:/home/erin:/bin/bash\n"
)


def test_users_db_directory_exists():
    """
    The directory /home/user/data/users_db must exist before the task begins.
    """
    assert DATA_DIR.is_dir(), (
        f"Required directory missing: {DATA_DIR}. "
        "The test cannot proceed without the user database directory."
    )


def test_passwd_file_exists_and_exact_content():
    """
    The passwd.txt file must exist and contain exactly the expected lines,
    including the trailing newline on the last line.
    """
    assert PASSWD_FILE.is_file(), (
        f"Required file missing: {PASSWD_FILE}. "
        "The task description specifies that this file must already be present."
    )

    actual_content = PASSWD_FILE.read_text(encoding="utf-8")
    assert actual_content == EXPECTED_PASSWD_CONTENT, (
        "The contents of passwd.txt do not match the expected initial state.\n\n"
        "Expected:\n"
        f"{EXPECTED_PASSWD_CONTENT!r}\n\n"
        "Found:\n"
        f"{actual_content!r}"
    )


def test_account_summary_log_not_present_yet():
    """
    The output file should NOT exist before the student performs the task.
    Its presence would indicate the task was run prematurely.
    """
    assert not SUMMARY_FILE.exists(), (
        f"The file {SUMMARY_FILE} already exists, but it should only be created "
        "by the student's solution command.  Remove or rename it before running "
        "the task."
    )