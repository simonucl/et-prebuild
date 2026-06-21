# test_initial_state.py
#
# This test-suite validates that the operating-system / filesystem
# is in the correct “starting” state *before* the student performs
# any actions for the “account summary” exercise.
#
# What we check:
#   1. /home/user/logs exists, is a directory, and has mode 755.
#   2. /home/user/logs/site_admin.log exists, is a regular file,
#      and contains exactly the 10 expected lines (including the
#      final trailing newline).
#   3. /home/user/logs/account_summary.log must NOT exist yet.
#
# If any assertion fails, the message will clearly indicate what
# is missing or incorrect.
#
# Only the Python standard library and pytest are used.

import os
import stat
import pytest

LOG_DIR = "/home/user/logs"
ADMIN_LOG = os.path.join(LOG_DIR, "site_admin.log")
SUMMARY_LOG = os.path.join(LOG_DIR, "account_summary.log")

EXPECTED_ADMIN_LOG_LINES = [
    "2024-05-25 09:12:30 useradd alice\n",
    "2024-05-25 09:15:02 useradd bob\n",
    "2024-05-25 09:16:45 passwd alice SUCCESS\n",
    "2024-05-25 09:18:07 passwd alice SUCCESS\n",
    "2024-05-25 09:20:13 passwd bob FAILURE: password too short\n",
    "2024-05-25 09:22:50 passwd bob SUCCESS\n",
    "2024-05-25 09:30:00 userdel dave\n",
    "2024-05-25 09:35:12 passwd dave FAILURE: user not found\n",
    "2024-05-25 10:00:00 useradd eve\n",
    "2024-05-25 10:05:52 passwd eve SUCCESS\n",
]


def mode_bits(path):
    """Return the permission bits (e.g. 0o755) of path."""
    return stat.S_IMODE(os.stat(path).st_mode)


def test_log_directory_exists_and_permissions():
    assert os.path.isdir(LOG_DIR), (
        f"Required directory {LOG_DIR!r} is missing or is not a directory."
    )

    expected_mode = 0o755
    actual_mode = mode_bits(LOG_DIR)
    assert actual_mode == expected_mode, (
        f"{LOG_DIR!r} must have mode {oct(expected_mode)}, "
        f"but has {oct(actual_mode)}."
    )


def test_admin_log_file_contents():
    assert os.path.isfile(ADMIN_LOG), (
        f"Required log file {ADMIN_LOG!r} is missing."
    )

    # Read the entire file as binary so we can check trailing newline precisely.
    with open(ADMIN_LOG, "rb") as fh:
        data = fh.read()

    # Splitlines with keepends=True to retain newline characters.
    lines = data.splitlines(keepends=True)

    assert len(lines) == 10, (
        f"{ADMIN_LOG!r} must contain exactly 10 lines, found {len(lines)}."
    )

    # Compare expected and actual line by line for easier diff on failure.
    for idx, (expected, actual) in enumerate(zip(EXPECTED_ADMIN_LOG_LINES, lines), start=1):
        assert expected == actual.decode(), (
            f"Line {idx} of {ADMIN_LOG!r} is incorrect.\n"
            f"Expected: {expected!r}\n"
            f"Found   : {actual.decode()!r}"
        )


def test_summary_log_does_not_exist_yet():
    assert not os.path.exists(SUMMARY_LOG), (
        f"{SUMMARY_LOG!r} should NOT exist before the student runs their solution."
    )