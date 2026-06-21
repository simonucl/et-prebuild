# test_initial_state.py
#
# This test-suite validates that the filesystem is in the expected
# *initial* state, before the student carries out the task described in
# the assignment.  In particular, it confirms that no artefacts from the
# yet-to-be-performed work are present.

import os
import pytest
from pathlib import Path

HOME = Path("/home/user")
BENCHMARK_DIR = HOME / "benchmark"
RESULT_FILE = BENCHMARK_DIR / "result.json"


def test_home_directory_exists():
    """
    Sanity-check that the base home directory is present; this must be true
    regardless of the assignment.
    """
    assert HOME.is_dir(), (
        f"Expected the home directory {HOME} to exist, "
        "but it does not."
    )


def test_benchmark_directory_absent():
    """
    The assignment explicitly instructs the student to create a *fresh*
    directory called /home/user/benchmark.  Therefore, prior to their
    action, that directory must NOT yet exist.
    """
    assert not BENCHMARK_DIR.exists(), (
        f"The directory {BENCHMARK_DIR} already exists, but the task "
        "requires the student to create it.  Please remove it so the "
        "environment starts clean."
    )


def test_result_file_absent():
    """
    Likewise, the result.json file must not be present before the student
    runs the benchmark and writes the output.
    """
    assert not RESULT_FILE.exists(), (
        f"The file {RESULT_FILE} already exists, but the student is "
        "supposed to create it as part of the task.  Please ensure the "
        "filesystem is clean before grading."
    )