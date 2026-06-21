# test_initial_state.py
#
# Pytest suite that verifies the *initial* state of the filesystem
# before the student carries out the shell-task described in the
# assignment.  These checks make sure that the starting conditions
# are exactly as required—no more and no less—so that the follow-up
# grading logic (not part of this file) can rely on a known baseline.
#
# This file uses only the Python standard library + pytest.

import os
import stat
import textwrap
import pytest

HOME_DIR = "/home/user"
LEGACY_DIR = os.path.join(HOME_DIR, "legacy_build")
SCRIPT_PATH = os.path.join(LEGACY_DIR, "run_legacy_build.sh")
BUILD_LOGS_DIR = os.path.join(LEGACY_DIR, "build_logs")
BUILD_OUTPUT_LOG = os.path.join(BUILD_LOGS_DIR, "build_output.log")
BUILD_STATUS_LOG = os.path.join(BUILD_LOGS_DIR, "build_status.log")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def is_executable(mode: int) -> bool:
    """Return True if any of the executable bits are set in *mode*."""
    return bool(mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_legacy_directory_exists():
    assert os.path.isdir(
        LEGACY_DIR
    ), f"Required directory {LEGACY_DIR!r} is missing."

def test_script_presence_and_permissions():
    assert os.path.isfile(
        SCRIPT_PATH
    ), f"Expected script {SCRIPT_PATH!r} to exist but it is missing."

    st = os.stat(SCRIPT_PATH)
    mode = stat.S_IMODE(st.st_mode)

    # Script should NOT yet be executable (0644 by spec).
    assert not is_executable(
        mode
    ), (
        f"{SCRIPT_PATH} should NOT be executable at the start "
        f"(current mode {oct(mode)})."
    )

    # Owner should have read & write
    assert mode & stat.S_IRUSR, f"{SCRIPT_PATH} should be readable by owner."
    assert mode & stat.S_IWUSR, f"{SCRIPT_PATH} should be writable by owner."

def test_script_contents_are_exact():
    """
    The legacy build script must match the canonical, published
    content verbatim (ignoring a possible trailing newline).
    """
    expected_content = textwrap.dedent(
        """\
        #!/usr/bin/env bash
        echo "Starting legacy build pipeline..."
        sleep 1
        echo "Compiling module alpha..."
        sleep 1
        echo "Running unit tests..."
        sleep 1
        echo "All tests passed."
        sleep 1
        echo "BUILD SUCCESSFUL"
        """
    )

    with open(SCRIPT_PATH, "r", encoding="utf-8") as fp:
        actual_content = fp.read()

    assert (
        actual_content.strip() == expected_content.strip()
    ), (
        f"Contents of {SCRIPT_PATH} do not match the expected template.\n"
        "---- Expected (stripped) ----\n"
        f"{expected_content}\n"
        "---- Actual (stripped) ------\n"
        f"{actual_content.strip()}\n"
        "-----------------------------"
    )

def test_build_logs_directory_does_not_exist():
    assert not os.path.exists(
        BUILD_LOGS_DIR
    ), (
        f"Directory {BUILD_LOGS_DIR!r} should NOT exist at the beginning; "
        "it will be created by the student's solution."
    )

def test_no_preexisting_log_files():
    assert not os.path.exists(
        BUILD_OUTPUT_LOG
    ), f"{BUILD_OUTPUT_LOG!r} should not exist before the task is run."
    assert not os.path.exists(
        BUILD_STATUS_LOG
    ), f"{BUILD_STATUS_LOG!r} should not exist before the task is run."