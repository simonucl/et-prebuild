# test_initial_state.py
#
# This pytest suite validates that the operating-system state is **clean**
# before the student runs their solution.  Specifically, it checks that
# neither the benchmark directory (/home/user/perf) nor the benchmark CSV
# file (/home/user/perf/benchmark.csv) already exists.
#
# If any of these artefacts are present *before* the student begins, the
# tests will fail with a clear, actionable message.

import os
import stat
import pytest

HOME_DIR = "/home/user"
PERF_DIR = os.path.join(HOME_DIR, "perf")
CSV_FILE = os.path.join(PERF_DIR, "benchmark.csv")


def _path_readable(path: str) -> str:
    """
    Helper to return a human-readable description of a path’s current state.
    """
    if not os.path.exists(path):
        return f"Path '{path}' does NOT exist."
    st = os.stat(path)
    kind = "directory" if stat.S_ISDIR(st.st_mode) else "file"
    perms = oct(st.st_mode & 0o777)
    return f"{kind.capitalize()} exists with permissions {perms}."


def test_home_directory_exists_and_is_directory():
    """
    Sanity-check that /home/user exists and is a directory; this is a
    pre-condition for all later tasks.
    """
    assert os.path.exists(HOME_DIR), (
        "Expected the home directory '/home/user' to exist, "
        "but it does not."
    )
    assert os.path.isdir(HOME_DIR), (
        f"Expected '/home/user' to be a directory, "
        f"but found something else: {_path_readable(HOME_DIR)}"
    )


def test_perf_directory_absent_initially():
    """
    The performance benchmark directory should NOT exist prior to the
    student's action.  Its presence would indicate that the environment
    has been polluted by a previous run.
    """
    assert not os.path.exists(PERF_DIR), (
        "The directory '/home/user/perf' already exists BEFORE the benchmark "
        "has been executed.  The environment must start clean.\n"
        f"{_path_readable(PERF_DIR)}"
    )


def test_benchmark_csv_absent_initially():
    """
    The benchmark CSV file should NOT be present before the student's code
    runs.  If it exists now, the test environment is not in its expected
    pristine state.
    """
    assert not os.path.exists(CSV_FILE), (
        "The file '/home/user/perf/benchmark.csv' already exists BEFORE the "
        "benchmark has been executed.  The environment must start clean.\n"
        f"{_path_readable(CSV_FILE)}"
    )