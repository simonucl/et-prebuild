# test_initial_state.py
#
# This pytest suite validates the **initial** state of the operating-system /
# filesystem before the student starts working on the assignment.
#
# Nothing related to the final artefacts must exist yet; otherwise the task
# would already be (partially) solved and the instructions to “create” the
# resources would make no sense.
#
# The tests therefore assert **absence** of the datasets directory, the three
# numbers_*.txt files, and the benchmark_results.csv metadata file.
#
# If any of these items are found, the tests will fail with an explanatory
# message so that the student (or the course author) can reset the environment
# before grading begins.
#
# Only the Python standard library and pytest are used, as required.

import os
import stat
import pytest

HOME = "/home/user"
DATASETS_DIR = os.path.join(HOME, "datasets")
NUM_FILES = [
    os.path.join(DATASETS_DIR, "numbers_1000.txt"),
    os.path.join(DATASETS_DIR, "numbers_5000.txt"),
    os.path.join(DATASETS_DIR, "numbers_10000.txt"),
]
META_FILE = os.path.join(HOME, "benchmark_results.csv")


def test_home_directory_exists_and_is_writable():
    """Sanity-check: the /home/user directory itself must exist and be writable."""
    assert os.path.isdir(HOME), f"Required home directory {HOME!r} is missing."
    mode = os.stat(HOME).st_mode
    is_writable = bool(mode & stat.S_IWUSR)
    assert is_writable, f"Home directory {HOME!r} exists but is not writable by the current user."


@pytest.mark.parametrize("path", [DATASETS_DIR, *NUM_FILES, META_FILE])
def test_required_paths_do_not_exist_yet(path):
    """
    None of the target artefacts should exist before the student starts.
    If any of them are present, the environment is in an unexpected state and
    must be cleaned up.
    """
    assert not os.path.exists(
        path
    ), (
        f"Pre-existing artefact detected: {path!r}. "
        "The initial state must be empty so that the student can create it."
    )