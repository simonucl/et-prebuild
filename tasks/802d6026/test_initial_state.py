# test_initial_state.py
#
# This test-suite validates the *initial* state of the operating
# system / filesystem **before** the student performs any action
# for the “uptime-monitoring” exercise.
#
# It deliberately checks ONLY the prerequisites that must already
# exist, never the artefacts the student is asked to create
# (e.g. check_targets.list, parse.log).
#
# Requirements verified:
#   1. The directory /home/user/monitoring exists, is a directory,
#      and is writable by the current user.
#   2. The file /home/user/monitoring/monitors.ini exists,
#      is readable, and its contents *exactly* match
#      the specification given in the exercise statement.
#
# The tests rely solely on the Python standard library + pytest.

import os
import stat
import textwrap
import pytest

MONITORING_DIR = "/home/user/monitoring"
INI_PATH = os.path.join(MONITORING_DIR, "monitors.ini")

# --------------------------------------------------------------------------- #
# Helper: canonical expected content of monitors.ini (with exact newlines).
# --------------------------------------------------------------------------- #
EXPECTED_INI_CONTENT = textwrap.dedent(
    """\
    [web]
    url = https://example.com
    expected_status = 200

    [db]
    url = tcp://db.internal:5432
    expected_status = alive

    [cache]
    url = tcp://cache.internal:6379
    expected_status = alive
    """
)

# The block above deliberately ends with a single trailing newline,
# matching the specification verbatim.


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_monitoring_directory_exists_and_writable():
    """
    The /home/user/monitoring directory must exist, be a directory,
    and be writable by the current user.
    """
    assert os.path.exists(
        MONITORING_DIR
    ), f"Required directory {MONITORING_DIR!r} does not exist."

    assert os.path.isdir(
        MONITORING_DIR
    ), f"{MONITORING_DIR!r} exists but is not a directory."

    # Directory should be writable so the student can create new files in it.
    assert os.access(
        MONITORING_DIR, os.W_OK
    ), f"Directory {MONITORING_DIR!r} is not writable by the current user."


def test_monitoring_directory_permissions():
    """
    Directory permissions should be 755 (rwxr-xr-x) according to
    the exercise text.  If the executing environment forces a
    different umask this test will still allow more restrictive
    *group/other* bits (e.g. 750) but user (owner) permissions must
    include read, write and execute.
    """
    st_mode = os.stat(MONITORING_DIR).st_mode
    assert (
        st_mode & stat.S_IRUSR
    ), f"{MONITORING_DIR!r} is missing owner-read permission."
    assert (
        st_mode & stat.S_IWUSR
    ), f"{MONITORING_DIR!r} is missing owner-write permission."
    assert (
        st_mode & stat.S_IXUSR
    ), f"{MONITORING_DIR!r} is missing owner-execute permission."


def test_monitors_ini_exists_and_readable():
    """
    The monitors.ini file must exist and be readable.
    """
    assert os.path.isfile(
        INI_PATH
    ), f"Required file {INI_PATH!r} does not exist or is not a regular file."

    assert os.access(
        INI_PATH, os.R_OK
    ), f"File {INI_PATH!r} is not readable by the current user."


def test_monitors_ini_permissions():
    """
    monitors.ini should have mode 644 (rw-r--r--) as stated.
    We allow the environment to make it *more restrictive* (e.g. 640)
    but not less.
    """
    st_mode = os.stat(INI_PATH).st_mode

    # Owner must have read & write permissions
    assert (
        st_mode & stat.S_IRUSR
    ), f"{INI_PATH!r} is missing owner-read permission."
    assert (
        st_mode & stat.S_IWUSR
    ), f"{INI_PATH!r} is missing owner-write permission."

    # Group and Others must not have write permission
    assert not (
        st_mode & stat.S_IWGRP
    ), f"{INI_PATH!r} should not be group-writable (expected 644)."
    assert not (
        st_mode & stat.S_IWOTH
    ), f"{INI_PATH!r} should not be other-writable (expected 644)."


def test_monitors_ini_exact_contents():
    """
    monitors.ini must match the exact byte-for-byte payload
    described in the specification, including blank lines and
    the final trailing newline.
    """
    with open(INI_PATH, "r", encoding="utf-8") as fh:
        actual = fh.read()

    # Fail with a helpful diff-like output if the contents differ.
    if actual != EXPECTED_INI_CONTENT:
        diff_header = (
            "\nExpected content (repr):\n"
            f"{repr(EXPECTED_INI_CONTENT)}\n"
            "Actual content (repr):\n"
            f"{repr(actual)}\n"
        )
        pytest.fail(
            f"Contents of {INI_PATH!r} do not match the expected specification."
            + diff_header
        )