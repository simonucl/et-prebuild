# test_initial_state.py
#
# This pytest suite validates the *initial* state of the filesystem
# before the student carries out the backup task.  It deliberately
# avoids touching /home/user/backups or any other output locations.
#
# Expectations (truth values):
#   • /home/user/datasets exists and contains exactly four data files
#     arranged as shown below.
#   • Each file is 18 bytes long and contains the exact ASCII text
#     specified in the task description.
#
# Layout that must already be present:
#   /home/user/datasets/
#       images/img1.jpg   -> "fake image data 1\n"
#       images/img2.jpg   -> "fake image data 2\n"
#       labels/img1.txt   -> "label for image 1\n"
#       labels/img2.txt   -> "label for image 2\n"

import os
from pathlib import Path

import pytest

DATASET_ROOT = Path("/home/user/datasets")

# Relative path -> expected content (as text, including trailing newline)
EXPECTED_FILES = {
    "images/img1.jpg": "fake image data 1\n",
    "images/img2.jpg": "fake image data 2\n",
    "labels/img1.txt": "label for image 1\n",
    "labels/img2.txt": "label for image 2\n",
}

@pytest.fixture(scope="module")
def dataset_root():
    """Return the Path object for the dataset root."""
    return DATASET_ROOT


def test_dataset_directory_exists(dataset_root):
    assert dataset_root.exists(), (
        f"Required directory {dataset_root} is missing. "
        "Make sure the initial dataset is in place."
    )
    assert dataset_root.is_dir(), f"{dataset_root} exists but is not a directory."


def test_required_subdirectories_exist(dataset_root):
    for subdir in ("images", "labels"):
        d = dataset_root / subdir
        assert d.exists() and d.is_dir(), (
            f"Expected sub-directory {d} is missing. "
            "The cleaned dataset should already be organised into "
            "'images' and 'labels' folders."
        )


def test_expected_files_present(dataset_root):
    for rel_path in EXPECTED_FILES:
        abs_path = dataset_root / rel_path
        assert abs_path.exists() and abs_path.is_file(), (
            f"Expected file {abs_path} is missing."
        )


def test_no_extra_files(dataset_root):
    """Ensure there are *exactly* four data files under the dataset root."""
    discovered = [
        str(p.relative_to(dataset_root))
        for p in dataset_root.rglob("*")
        if p.is_file()
    ]
    assert sorted(discovered) == sorted(EXPECTED_FILES.keys()), (
        "The dataset should contain exactly the four files specified.\n"
        f"Expected: {sorted(EXPECTED_FILES.keys())}\n"
        f"Found   : {sorted(discovered)}"
    )


@pytest.mark.parametrize("rel_path,expected_text", EXPECTED_FILES.items())
def test_file_size_and_content(dataset_root, rel_path, expected_text):
    abs_path = dataset_root / rel_path
    size = abs_path.stat().st_size
    assert size == 18, (
        f"{abs_path} should be 18 bytes but is {size} bytes. "
        "Verify that the file contents match the specification."
    )

    # Read as binary to avoid platform newline translation, then decode
    data = abs_path.read_bytes().decode("ascii")
    assert data == expected_text, (
        f"Contents of {abs_path} do not match expectation.\n"
        f"Expected: {repr(expected_text)}\n"
        f"Found   : {repr(data)}"
    )