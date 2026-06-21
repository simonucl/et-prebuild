# test_initial_state.py
#
# This pytest suite validates the *initial* operating-system / filesystem
# state *before* the student carries out the benchmark task.
#
# It intentionally checks that:
#   1. The benchmark target (/bin/true) exists and is executable.
#   2. No pre-existing compliance log is present, so the student must
#      create it themselves.
#
# If any of these assertions fail, the error messages explain exactly
# what is wrong.

import os
import stat
import pytest

BENCHMARK_CMD = "/bin/true"
LOG_DIR = "/home/user/benchmark_logs"
LOG_FILE = os.path.join(LOG_DIR, "performance_policy.log")


def test_bin_true_exists_and_is_executable():
    """
    Verify that /bin/true exists and is an executable file.
    """
    assert os.path.isfile(
        BENCHMARK_CMD
    ), f"Expected benchmark command '{BENCHMARK_CMD}' to be a file, but it does not exist."

    # Check the execute bit for the current user
    is_executable = os.access(BENCHMARK_CMD, os.X_OK)
    mode = oct(os.stat(BENCHMARK_CMD).st_mode & 0o777)
    assert is_executable, (
        f"File '{BENCHMARK_CMD}' exists but is not executable. "
        f"Current mode is {mode}."
    )


def test_compliance_log_does_not_exist_yet():
    """
    The compliance log must NOT exist before the student runs their solution.
    Its presence would indicate that the benchmark has already been executed.
    """
    assert not os.path.exists(
        LOG_FILE
    ), (
        f"The compliance log '{LOG_FILE}' already exists. "
        "The initial state should be clean so the student can create it."
    )