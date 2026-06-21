# test_initial_state.py
#
# This pytest suite validates the *initial* state of the filesystem
# before the student performs any actions.  It checks that the rotation
# directory and the original log file exist and that the log file
# contains the exact seven lines (with newlines) described in the prompt.
#
# NOTE:  The tests intentionally *do not* look for the output artefact
#        (/home/user/rotation/leaked_old_passwords.tsv) because that file
#        should not exist yet.

import os
import pytest

ROTATION_DIR = "/home/user/rotation"
LOG_PATH = os.path.join(ROTATION_DIR, "credential_rotation.log")

EXPECTED_LINES = [
    "[2024-05-03 09:14:02] user=alice action=update password_old=2c1743a password_new=10ac5bd\n",
    "[2024-05-03 09:15:45] user=alice action=confirm rotation_status=success\n",
    "[2024-05-03 10:01:11] user=bob action=update password_old=ffab23a password_new=946adfe\n",
    "[2024-05-03 10:03:02] user=bob action=confirm rotation_status=success\n",
    "[2024-05-03 11:20:55] user=charlie action=update password_old=ab41dfe password_new=dfee551\n",
    "[2024-05-03 11:22:11] user=charlie action=confirm rotation_status=success\n",
    "[2024-05-03 12:10:13] user=david action=confirm rotation_status=success\n",
]

@pytest.fixture(scope="module")
def log_contents():
    """Read and return the contents of the rotation log as a list of lines."""
    if not os.path.isfile(LOG_PATH):
        pytest.skip(f"Expected log file not found at {LOG_PATH}")
    with open(LOG_PATH, "r", encoding="utf-8") as fp:
        return fp.readlines()


def test_rotation_directory_exists():
    assert os.path.isdir(
        ROTATION_DIR
    ), f"Required directory {ROTATION_DIR!r} is missing or not a directory."


def test_log_file_exists_and_is_file():
    assert os.path.isfile(
        LOG_PATH
    ), f"Required log file {LOG_PATH!r} is missing or not a regular file."


def test_log_file_exact_content(log_contents):
    # 1. Exact number of lines.
    assert len(log_contents) == 7, (
        f"Expected 7 lines in {LOG_PATH!r}, found {len(log_contents)}."
    )

    # 2. Every line must terminate with '\n'.
    for idx, line in enumerate(log_contents, start=1):
        assert line.endswith(
            "\n"
        ), f"Line {idx} of {LOG_PATH!r} is missing a terminating newline."

    # 3. File content must match the expected canonical lines exactly.
    assert log_contents == EXPECTED_LINES, (
        "Contents of the log file do not match the expected initial state.\n\n"
        "---------- Expected ----------\n"
        + "".join(EXPECTED_LINES)
        + "\n---------- Found ----------\n"
        + "".join(log_contents)
    )


def test_log_file_contains_exactly_three_password_old_events(log_contents):
    count = sum("password_old=" in line for line in log_contents)
    assert count == 3, (
        f"Expected exactly 3 lines containing 'password_old=' in "
        f"{LOG_PATH!r}, found {count}."
    )