# test_initial_state.py
#
# Pytest suite to validate the *initial* state of the operating system /
# filesystem before the learner performs any work on the exercise
# “Android build log ‑ WARNING extraction”.
#
# The tests assert that:
#   1. The build-logs directory exists with the correct permissions.
#   2. The original Android build log exists, is readable, has the correct
#      permissions and contains the exact expected text.
#   3. The WARNING-summary file that the learner is supposed to create
#      does *not* exist yet.
#
# Only the Python standard library and pytest are used.

import os
import stat
import hashlib
import textwrap
import pytest

HOME = "/home/user"
BUILD_LOG_DIR = os.path.join(HOME, "build_logs")
SOURCE_LOG = os.path.join(BUILD_LOG_DIR, "android_build_2023-11-01.log")
SUMMARY_FILE = os.path.join(BUILD_LOG_DIR, "warning_summary_2023-11-01.txt")

EXPECTED_LOG_CONTENT = textwrap.dedent(
    """\
    [2023-11-01 10:00:00] INFO: Build started
    [2023-11-01 10:00:05] WARNING: Deprecated API usage in module 'auth'
    [2023-11-01 10:00:10] INFO: Compiling resources
    [2023-11-01 10:00:12] WARNING: Unused variable in file MainActivity.kt
    [2023-11-01 10:00:15] ERROR: Compilation failed
    [2023-11-01 10:00:20] INFO: Build finished with errors
    """
).encode()  # keep the trailing newline added by textwrap.dedent

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------
def _get_mode(path):
    """Return the permission bits (e.g. 0o755, 0o644) of a filesystem object."""
    return stat.S_IMODE(os.stat(path).st_mode)


# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------
def test_build_logs_directory_exists_and_mode():
    assert os.path.isdir(BUILD_LOG_DIR), (
        f"Expected directory {BUILD_LOG_DIR!r} to exist, "
        "but it is missing."
    )

    mode = _get_mode(BUILD_LOG_DIR)
    expected = 0o755
    assert mode == expected, (
        f"Directory {BUILD_LOG_DIR!r} should have mode {oct(expected)}, "
        f"but has {oct(mode)} instead."
    )


def test_source_log_exists_is_readable_and_correct():
    assert os.path.isfile(SOURCE_LOG), (
        f"Expected source log {SOURCE_LOG!r} to exist, but it is missing."
    )

    assert os.access(SOURCE_LOG, os.R_OK), (
        f"Source log {SOURCE_LOG!r} exists but is not readable."
    )

    mode = _get_mode(SOURCE_LOG)
    expected_mode = 0o644
    assert mode == expected_mode, (
        f"Source log {SOURCE_LOG!r} should have mode {oct(expected_mode)}, "
        f"but has {oct(mode)} instead."
    )

    # Read and compare the exact bytes
    with open(SOURCE_LOG, "rb") as fp:
        data = fp.read()

    assert data == EXPECTED_LOG_CONTENT, (
        "The content of the source log does not match the expected text.\n"
        "If the file was changed or truncated, restore it before continuing."
    )

    # A secondary guard: if the author of the exercise provided a byte-count,
    # keep it in sync.  This gives an extra, easy-to-read hint on failure.
    expected_size = len(EXPECTED_LOG_CONTENT)
    actual_size = len(data)
    assert actual_size == expected_size, (
        f"Expected source log size to be {expected_size} bytes, "
        f"but got {actual_size} bytes."
    )


def test_summary_file_does_not_exist_yet():
    assert not os.path.exists(SUMMARY_FILE), (
        f"The summary file {SUMMARY_FILE!r} already exists, but it should "
        "not be present before the student generates it."
    )