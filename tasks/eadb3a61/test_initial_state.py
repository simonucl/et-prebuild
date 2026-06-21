# test_initial_state.py
#
# This test-suite verifies the initial OS / filesystem state
# BEFORE the student runs any commands.
#
# It checks only the pre-existing items and intentionally
# avoids touching the location where the student will write
# their results.

import os
import stat
import textwrap

import pytest


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _assert_dir(path, min_mode=0o755):
    """
    Assert that `path` exists, is a directory and has at least `min_mode`
    permissions (POSIX).  Raises an assertion error with a clear message
    otherwise.
    """
    assert os.path.exists(path), f"Expected directory {path!r} to exist."
    assert os.path.isdir(path), f"Expected {path!r} to be a directory."

    # Only check mode bits on POSIX platforms
    if os.name == "posix":
        mode = stat.S_IMODE(os.stat(path).st_mode)
        assert mode & min_mode == min_mode, (
            f"Directory {path!r} has mode {oct(mode)}, "
            f"but needs at least {oct(min_mode)}."
        )


def _assert_file_content(path, expected):
    """
    Assert that file `path` exists and its entire content matches `expected`.
    """
    assert os.path.exists(path), f"Expected file {path!r} to exist."
    assert os.path.isfile(path), f"Expected {path!r} to be a regular file."

    with open(path, "r", encoding="utf-8") as fp:
        data = fp.read()

    assert data == expected, (
        f"Content of {path!r} does not match the expected initial content."
    )


# ---------------------------------------------------------------------------
# Fixtures / constants
# ---------------------------------------------------------------------------

BACKUP_DIR = "/home/user/backup"
LOGS_DIR = "/home/user/backup/logs"
RSYNC_LOG = "/home/user/backup/logs/rsync_2023-09-01.log"

EXPECTED_RSYNC_LOG = textwrap.dedent(
    """\
    2023/09/01 03:15:12 [12345] sent 123456 bytes  received 78910 bytes  total size 987654321
    2023/09/01 03:15:12 [12345] verify /data/projects/app1/bin/run.sh OK
    2023/09/01 03:15:12 [12345] verify /data/projects/app1/config/settings.yml FAILED checksum
    2023/09/01 03:15:13 [12345] verify /data/images/logo.png OK
    2023/09/01 03:15:13 [12345] verify /data/db/dump.sql FAILED size
    2023/09/01 03:15:13 [12345] verify /data/docs/readme.md OK
    2023/09/01 03:15:13 [12345] verify /data/secrets/keys.txt FAILED checksum
    """
)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_directories_exist_and_permissions():
    """
    Backup base directories must already be present with sensible permissions.
    NOTE: We do NOT test /home/user/backup/verification here because that
    directory will be used for the student's output.
    """
    _assert_dir(BACKUP_DIR, min_mode=0o755)
    _assert_dir(LOGS_DIR, min_mode=0o755)


def test_rsync_log_file_content():
    """
    The rsync verification log must already exist and contain exactly the
    expected lines (including the final newline).
    """
    # The EXPECTED_RSYNC_LOG string in the constant above ends with '\n'
    # (because textwrap.dedent keeps the trailing newline in the triple-quoted
    # literal).  This lets us verify that the file itself ends with a newline.
    assert EXPECTED_RSYNC_LOG.endswith("\n"), "Internal test error: expected string must end with a newline."

    _assert_file_content(RSYNC_LOG, EXPECTED_RSYNC_LOG)