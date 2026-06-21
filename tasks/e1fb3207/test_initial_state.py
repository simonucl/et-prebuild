# test_initial_state.py
#
# This pytest suite validates the *initial* state of the VM **before** the
# student creates the diagnostic bundle.  It checks that all expected sample
# log files are present (with the correct size properties) and that the
# “decoy” files called out in the task description also exist with the
# prescribed small size.  No tests touch, require, or even mention the future
# output directory /home/user/diagnostics.

import os
import stat
import pytest

HOME = "/home/user"

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _assert_regular_file(path: str) -> os.stat_result:
    """
    Assert that `path` exists and is a regular file.
    Returns the os.stat_result for further inspection.
    """
    assert os.path.exists(path), f"Expected file '{path}' is missing."
    st = os.stat(path)
    assert stat.S_ISREG(st.st_mode), f"'{path}' exists but is not a regular file."
    return st


# ---------------------------------------------------------------------------
# Parametrised test tables
# ---------------------------------------------------------------------------

# Files that MUST be ≥1024 bytes (qualifying logs)
QUALIFYING_FILES = [
    "/home/user/app1/logs/server.log",
    "/home/user/app1/logs/access.log",
    "/home/user/app2/logs/error.txt",
    "/home/user/app2/logs/trace.log",
    "/home/user/archive/old.log",
]

# Files that MUST be <1024 bytes (non-qualifying decoys)
DECOY_FILES_SMALL = [
    "/home/user/app1/logs/debug-20230802.log",
    "/home/user/app2/logs/README.md",
    "/home/user/app3/data/datafile.log",
]


# ---------------------------------------------------------------------------
# Tests for qualifying log files
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("filepath", QUALIFYING_FILES)
def test_qualifying_files_exist_and_large(filepath):
    """
    Each qualifying log file must exist, be a regular file, and be ≥1024 bytes.
    """
    st = _assert_regular_file(filepath)
    assert (
        st.st_size >= 1024
    ), f"File '{filepath}' should be at least 1024 bytes, but has size {st.st_size}."


# ---------------------------------------------------------------------------
# Tests for decoy files
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("filepath", DECOY_FILES_SMALL)
def test_decoy_files_exist_and_small(filepath):
    """
    Decoy files must exist but **not** satisfy the size requirement (they are
    intentionally small so they should *not* be gathered later).
    """
    st = _assert_regular_file(filepath)
    assert (
        st.st_size < 1024
    ), f"Decoy file '{filepath}' should be smaller than 1024 bytes; size is {st.st_size}."


# ---------------------------------------------------------------------------
# Sanity-check directories (helps pinpoint student mistakes early)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "dir_path",
    [
        "/home/user/app1/logs",
        "/home/user/app2/logs",
        "/home/user/app3/data",
        "/home/user/archive",
    ],
)
def test_expected_directories_exist(dir_path):
    """
    The directory hierarchy referenced by the task must already be on disk.
    """
    assert os.path.isdir(
        dir_path
    ), f"Required directory '{dir_path}' is missing or not a directory."