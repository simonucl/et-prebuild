# test_initial_state.py
#
# This pytest suite validates that the **initial** filesystem state
# (i.e. before the student has executed any solution code) is correct.
#
# What we verify:
#   • The expected source *.log files exist under /home/user/data/projects/.
#   • Each of those files has the exact byte-size specified in the task.
#   • Some representative non-log files also exist (to ensure they are
#     not mistakenly removed beforehand).
#   • The destination directory /home/user/archives/ exists and is writable.
#
# IMPORTANT
#   We deliberately do *not* check for the presence or absence of any
#   output artefacts such as:
#       /home/user/archives/old_logs_snap.tar.gz
#       /home/user/archives/old_logs_snap.report
#   Doing so would violate the “DO NOT test for any of the output files
#   or directories” rule, because those paths are meant to be produced
#   by the student solution, not to exist beforehand.

import os
import stat
import pytest

HOME = "/home/user"
SRC_ROOT = os.path.join(HOME, "data", "projects")
ARCHIVES_DIR = os.path.join(HOME, "archives")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def must_exist(path, what="file"):
    """Assert that *path* exists and is of the required type."""
    if what == "file":
        assert os.path.isfile(path), f"Expected file at {path!r} is missing."
    elif what == "dir":
        assert os.path.isdir(path), f"Expected directory at {path!r} is missing."
    else:
        raise ValueError(f"Unknown type {what!r}")


# ---------------------------------------------------------------------------
# Test cases
# ---------------------------------------------------------------------------

def test_source_log_files_present_and_sized_correctly():
    """
    Verify that each required *.log file is present under the source tree
    with its exact expected size (in bytes).
    """
    expected_logs = {
        # relative_path : expected_size
        "projA/app.log":               45,
        "projA/debug.log":             42,
        "projA/subdir/legacy.log":     22,
        "projB/server.log":            46,
    }

    for rel_path, expected_size in expected_logs.items():
        abs_path = os.path.join(SRC_ROOT, rel_path)
        must_exist(abs_path, "file")

        actual_size = os.path.getsize(abs_path)
        assert actual_size == expected_size, (
            f"{abs_path!r} has size {actual_size} bytes; expected {expected_size} bytes."
        )


def test_sample_non_log_files_exist():
    """
    The task statement mentions that some non-log files exist and must be left
    untouched.  We check that at least the given sample files are indeed present.
    """
    non_log_examples = [
        "projA/notes.txt",
        "projB/readme.md",
    ]
    for rel_path in non_log_examples:
        abs_path = os.path.join(SRC_ROOT, rel_path)
        must_exist(abs_path, "file")


def test_archives_directory_exists_and_writable():
    """
    The destination directory /home/user/archives must exist *before* the
    student solution runs, and it must be writable by the current user.
    """
    must_exist(ARCHIVES_DIR, "dir")

    # Check write permission for the current user.
    mode = os.stat(ARCHIVES_DIR).st_mode
    is_writable = bool(mode & stat.S_IWUSR)
    assert is_writable, f"Directory {ARCHIVES_DIR!r} exists but is not writable by the user."