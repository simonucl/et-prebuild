# test_initial_state.py
#
# Pytest checks that the *initial* filesystem state (before the student’s
# maintenance script runs) matches the specification that the automated
# grader relies on.  Any divergence means the test-bed is broken or the
# student has already altered the workspace and must be reset.

import os
import stat
import pytest

HOME = "/home/user"

# --------------------------------------------------------------------------- #
# Helper functions                                                            #
# --------------------------------------------------------------------------- #
def _assert_is_regular_file(path, msg):
    assert os.path.exists(path), f"Missing required file: {path}. {msg}"
    assert os.path.isfile(path), f"Expected a regular file at {path}, but found something else. {msg}"

def _assert_file_size(path, expected_bytes):
    size = os.path.getsize(path)
    assert size == expected_bytes, (
        f"File {path} has size {size} bytes, expected {expected_bytes} bytes."
    )

# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #

def test_required_directories_exist_and_empty():
    """
    /home/user/maintenance must already exist and be empty.
    """
    maint_dir = os.path.join(HOME, "maintenance")
    assert os.path.isdir(maint_dir), (
        f"Required directory {maint_dir} is missing. "
        "Create it (mode 0755) before running any maintenance tasks."
    )
    contents = os.listdir(maint_dir)
    assert contents == [], (
        f"Directory {maint_dir} is expected to be empty at the start, "
        f"but contains: {contents}.  Restore the clean initial state."
    )

@pytest.mark.parametrize(
    "path,expected_size",
    [
        ("/home/user/cicd_workspace/build_logs/build1.log", 1_536_000),
        ("/home/user/cicd_workspace/build_logs/build2.log",   512_000),
        ("/home/user/cicd_workspace/build_logs/build3.log", 2_097_152),
    ],
)
def test_build_logs_present_with_correct_size(path, expected_size):
    """
    Three .log files with exact byte counts must be present before any action.
    """
    _assert_is_regular_file(path, "Build log expected to exist before compression.")
    _assert_file_size(path, expected_size)

@pytest.mark.parametrize(
    "path",
    [
        "/home/user/cicd_workspace/build_logs/build1.log.gz",
        "/home/user/cicd_workspace/build_logs/build3.log.gz",
    ],
)
def test_no_compressed_logs_exist_yet(path):
    """
    Compressed .gz files must NOT exist before the student runs the solution.
    """
    assert not os.path.exists(path), (
        f"Unexpected file {path} found.  Initial state must not contain any "
        f"compressed logs.  Reset the workspace."
    )

@pytest.mark.parametrize(
    "path",
    [
        "/home/user/cicd_workspace/build_logs/old_build.tmp",
        "/home/user/cicd_workspace/test_results/testrun1.tmp",
        "/home/user/cicd_workspace/test_results/testrun2.tmp",
        "/home/user/cicd_workspace/artifacts/dist/artifact.tmp",
    ],
)
def test_tmp_files_exist_initially(path):
    """
    All *.tmp artefacts must be present before the clean-up step.
    """
    _assert_is_regular_file(path, "Temporary file expected to exist before purge.")

@pytest.mark.parametrize(
    "path",
    [
        "/home/user/maintenance/tmp_purge.log",
        "/home/user/maintenance/log_compress.log",
        "/home/user/maintenance/maintenance_summary.txt",
    ],
)
def test_no_maintenance_logs_present_yet(path):
    """
    No maintenance logs should exist prior to the student’s script.
    """
    assert not os.path.exists(path), (
        f"Unexpected pre-existing file {path}.  The maintenance logs are "
        f"generated *after* the script runs; remove or reset the file."
    )