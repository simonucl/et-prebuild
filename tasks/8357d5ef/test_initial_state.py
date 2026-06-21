# test_initial_state.py
#
# This test-suite validates that the *initial* filesystem state inside the
# grading container matches the specification given in the task description.
#
# IMPORTANT:  These tests examine **only** the pre-existing datasets that the
#             student’s command will later analyse.  They intentionally **do
#             NOT** touch any of the output locations such as
#             /home/user/reports or /home/user/reports/dataset_usage.log
#             (per the “DO NOT test for any of the output files or directories”
#             requirement).
#
# If any of the assertions below fail, it means the container has been
# provisioned incorrectly and the learner would be set up for failure even
# before writing any code or running any commands.

import os
from pathlib import Path

import pytest


HOME = Path("/home/user")
DATASETS_DIR = HOME / "datasets"

# Expected directory and file layout, including exact byte sizes.
# The sizes come from the public problem statement.
EXPECTED_LAYOUT = {
    "images": {
        "img.bin": 2_048_000,   # bytes
    },
    "texts": {
        "story.txt": 1_048_576,  # bytes
    },
    "videos": {
        "clip.mkv": 5_242_880,   # bytes
    },
}


@pytest.fixture(scope="module")
def datasets_path() -> Path:
    """Ensure /home/user/datasets exists and return its Path object."""
    assert DATASETS_DIR.exists(), (
        f"Required directory {DATASETS_DIR} is missing. "
        "The grader expects it to exist before the student runs any commands."
    )
    assert DATASETS_DIR.is_dir(), (
        f"{DATASETS_DIR} exists but is not a directory."
    )
    return DATASETS_DIR


def test_expected_subdirectories_exist(datasets_path: Path):
    """
    Verify that the first-level sub-directories required by the task
    (images, texts, videos) exist inside /home/user/datasets.
    """
    for subdir in EXPECTED_LAYOUT:
        p = datasets_path / subdir
        assert p.exists(), (
            f"Expected sub-directory {p} is missing. "
            "The student’s command relies on its presence."
        )
        assert p.is_dir(), f"{p} exists but is not a directory."


def test_expected_files_exist_and_have_correct_size(datasets_path: Path):
    """
    For each expected first-level sub-directory, check that the specified file
    exists and matches the exact byte size stated in the task description.
    """
    for subdir, files in EXPECTED_LAYOUT.items():
        for filename, expected_size in files.items():
            fpath = datasets_path / subdir / filename
            assert fpath.exists(), (
                f"Expected file {fpath} is missing."
            )
            assert fpath.is_file(), f"{fpath} exists but is not a regular file."

            # Validate file size in bytes.
            actual_size = fpath.stat().st_size
            assert actual_size == expected_size, (
                f"File {fpath} has size {actual_size} bytes, "
                f"expected {expected_size} bytes."
            )