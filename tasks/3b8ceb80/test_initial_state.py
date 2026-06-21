# test_initial_state.py
#
# This pytest suite validates the *initial* operating-system state
# before the student starts solving the task.  It makes sure that
# the credential-rotation source log is present with the exact
# expected contents and that the working directory is writable.

import os
import stat
import pytest

HOME = "/home/user"
CREDENTIALS_DIR = os.path.join(HOME, "credentials")
ROTATIONS_LOG = os.path.join(CREDENTIALS_DIR, "rotations.log")

# Expected exact contents of /home/user/credentials/rotations.log
EXPECTED_LINES = [
    "alice\n",
    "bob\n",
    "charlie\n",
    "alice\n",
    "alice\n",
    "bob\n",
    "dave\n",
    "eve\n",
    "bob\n",
    "frank\n",
]


def test_credentials_directory_exists_and_writable():
    """
    The directory /home/user/credentials must exist and be writable
    by the current user so that the solution script can create
    rotation_frequency.txt later.
    """
    assert os.path.isdir(CREDENTIALS_DIR), (
        f"Required directory {CREDENTIALS_DIR!r} is missing."
    )
    # Check write permission by current user
    is_writable = os.access(CREDENTIALS_DIR, os.W_OK)
    assert is_writable, (
        f"Directory {CREDENTIALS_DIR!r} is not writable by the current user."
    )


def test_rotations_log_exists_with_exact_contents():
    """
    Verify that the source log exists and its contents are *exactly*
    the 10 expected newline-terminated usernames with no extra blank
    lines or trailing spaces.
    """
    assert os.path.isfile(ROTATIONS_LOG), (
        f"Required file {ROTATIONS_LOG!r} is missing."
    )

    with open(ROTATIONS_LOG, "r", encoding="utf-8") as f:
        actual_lines = f.readlines()

    # 1. Exact line count
    assert len(actual_lines) == len(EXPECTED_LINES), (
        f"{ROTATIONS_LOG!r} should contain {len(EXPECTED_LINES)} lines but "
        f"has {len(actual_lines)}."
    )

    # 2. Exact line-by-line comparison
    for idx, (expected, actual) in enumerate(zip(EXPECTED_LINES, actual_lines), start=1):
        assert actual == expected, (
            f"Line {idx} in {ROTATIONS_LOG!r} differs.\n"
            f"Expected: {expected!r}\n"
            f"Actual:   {actual!r}"
        )

    # 3. Ensure the last character in the file is a newline character
    #    (i.e., the last entry is newline-terminated, but no blank lines follow).
    with open(ROTATIONS_LOG, "rb") as f:
        f.seek(-1, os.SEEK_END)
        last_byte = f.read(1)
    assert last_byte == b"\n", (
        f"The last character of {ROTATIONS_LOG!r} must be a newline (\\n)."
    )