# test_initial_state.py
"""
pytest suite that verifies the operating-system state *before* the student runs
their solution script.  At this point none of the benchmark artefacts should
exist yet.

If any of the paths below already exist, the tests will fail with a clear
message so the learner immediately knows that they are starting from an
unexpected state.
"""

import os
import stat
import pytest

HOME = "/home/user"
BENCH_DIR = os.path.join(HOME, "benchmark_logs")
LOG_FILE = os.path.join(BENCH_DIR, "incident_2023_001.log")
SUMMARY_FILE = os.path.join(BENCH_DIR, "summary.txt")


def _exists_msg(path: str) -> str:
    if os.path.islink(path):
        return f"Found an unexpected symlink at: {path}"
    try:
        st = os.lstat(path)
    except FileNotFoundError:
        return ""  # path truly does not exist
    kind = "directory" if stat.S_ISDIR(st.st_mode) else "file"
    return f"Found an unexpected {kind} at: {path}"


@pytest.mark.parametrize(
    "path",
    [
        BENCH_DIR,
        LOG_FILE,
        SUMMARY_FILE,
    ],
)
def test_paths_absent_before_student_action(path):
    """
    None of the benchmark directories or files should exist yet.
    """
    assert not os.path.exists(path), _exists_msg(path)