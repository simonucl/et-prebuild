# test_initial_state.py
#
# This pytest suite validates the *initial* state of the filesystem for the
# “current_data”-symlink exercise.  It is executed **before** students attempt
# any changes, ensuring the starting point is exactly as the problem statement
# describes.

import os
import stat
import pytest

HOME = "/home/user"
DATA_DIR = os.path.join(HOME, "data")
OUTPUT_DIR = os.path.join(HOME, "output")

DATASET_V1 = os.path.join(DATA_DIR, "dataset_v1")
DATASET_V2 = os.path.join(DATA_DIR, "dataset_v2")
DATASET_V3 = os.path.join(DATA_DIR, "dataset_v3")

SYMLINK_PATH = os.path.join(DATA_DIR, "current_data")
LOG_FILE = os.path.join(OUTPUT_DIR, "symlink_log.txt")


@pytest.mark.parametrize(
    "path",
    [
        DATA_DIR,
        DATASET_V1,
        DATASET_V2,
        DATASET_V3,
        OUTPUT_DIR,
    ],
)
def test_required_directories_exist_and_are_dirs(path):
    """
    All required directories must exist and be real directories (not symlinks).
    """
    assert os.path.exists(
        path
    ), f"Required directory {path!r} is missing."
    assert os.path.isdir(
        path
    ), f"Path {path!r} should be a directory but is not."
    # Ensure it is not a symlink to something else
    st_mode = os.lstat(path).st_mode
    assert not stat.S_ISLNK(
        st_mode
    ), f"Directory {path!r} should be a real directory, not a symlink."


def test_dataset_directories_are_initially_empty():
    """
    The dataset_v* directories are expected to be empty at the start.
    """
    for d in (DATASET_V1, DATASET_V2, DATASET_V3):
        contents = os.listdir(d)
        assert (
            len(contents) == 0
        ), f"Directory {d!r} should be empty but contains: {contents}"


def test_symlink_does_not_exist_initially():
    """
    No file/dir/symlink named `current_data` should exist yet.
    """
    assert not os.path.exists(
        SYMLINK_PATH
    ), f"{SYMLINK_PATH!r} should NOT exist before the student creates it."


def test_log_file_does_not_exist_initially():
    """
    The verification log should not exist until the student creates it.
    """
    assert not os.path.exists(
        LOG_FILE
    ), f"{LOG_FILE!r} should NOT exist in the initial state."