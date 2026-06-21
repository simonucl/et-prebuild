# test_initial_state.py
#
# This test-suite verifies that the workspace is still in its pristine
# “pre-task” state.  Nothing that the student is supposed to create during
# the assignment may exist yet.  Should any of the asserted paths already
# exist, the test will fail with an explanatory message so that the student
# knows which artefact must *not* be present at this stage.

import os
from pathlib import Path
import pytest

HOME = Path("/home/user")
BENCHMARK_DIR = HOME / "benchmarks"

INPUT_FILE = BENCHMARK_DIR / "testfile.bin"
COMPRESSED_FILES = [
    BENCHMARK_DIR / "testfile.bin.gz",
    BENCHMARK_DIR / "testfile.bin.bz2",
    BENCHMARK_DIR / "testfile.bin.xz",
]
CSV_FILE = BENCHMARK_DIR / "compression_benchmark.csv"


def _assert_absent(p: Path):
    """Helper that raises an informative assertion if the path exists."""
    assert not p.exists(), (
        f"The path {p} already exists, but it should **not** be present "
        f"before you start the assignment. Remove it and start over."
    )


def test_benchmark_directory_absent():
    """
    The /home/user/benchmarks directory must NOT exist yet.
    The student will create it as the very first step.
    """
    _assert_absent(BENCHMARK_DIR)


@pytest.mark.parametrize("path", [INPUT_FILE, *COMPRESSED_FILES, CSV_FILE])
def test_task_related_files_absent(path):
    """
    None of the files that belong to the assignment should exist before the
    student runs their solution script/commands.
    """
    _assert_absent(path)